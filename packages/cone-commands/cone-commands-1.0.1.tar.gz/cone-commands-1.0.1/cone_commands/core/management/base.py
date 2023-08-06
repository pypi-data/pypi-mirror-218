"""
Base classes for writing management commands (named commands which can
be executed through ``django-admin`` or ``manage.py``).
"""
import re
import requests
import argparse
import json
import os
import sys
from urllib.parse import urljoin
from argparse import ArgumentParser, HelpFormatter
from functools import partial
from io import TextIOBase
from cone_commands.core.management.color import color_style, no_style
from cone_commands.conf.global_settings import CONFIG_PATH
from cone.utils.classes import ClassManager
from cone.utils.functional import classproperty
from cone_commands.core.status import CommandStatus
from typing import Union, List, Dict

Command = ClassManager(name="Command",
                       path=[
                           "cone_commands.contrib",
                           "cone_commands.core.management.commands"
                       ],
                       unique_keys=['command_name'],
                       )


ALL_CHECKS = "__all__"


class CommandError(Exception):
    """
    Exception class indicating a problem while executing a management
    command.

    If this exception is raised during the execution of a management
    command, it will be caught and turned into a nicely-printed error
    message to the appropriate output stream (i.e., stderr); as a
    result, raising this exception (with a sensible description of the
    error) is the preferred way to indicate that something has gone
    wrong in the execution of a command.
    """

    def __init__(self, *args, returncode=1, **kwargs):
        self.returncode = returncode
        super().__init__(*args, **kwargs)


class SystemCheckError(CommandError):
    """
    The system check framework detected unrecoverable errors.
    """

    pass


class CommandParser(ArgumentParser):
    """
    Customized ArgumentParser class to improve some error messages and prevent
    SystemExit in several occasions, as SystemExit is unacceptable when a
    command is called programmatically.
    """

    def __init__(
        self, *, missing_args_message=None, called_from_command_line=None, **kwargs
    ):
        self.missing_args_message = missing_args_message
        self.called_from_command_line = called_from_command_line
        super().__init__(**kwargs)

    def parse_args(self, args=None, namespace=None):
        # Catch missing argument for a better error message
        if self.missing_args_message and not (
            args or any(not arg.startswith("-") for arg in args)
        ):
            self.error(self.missing_args_message)
        return super().parse_args(args, namespace)

    def error(self, message):
        if self.called_from_command_line:
            super().error(message)
        else:
            raise CommandError("Error: %s" % message)

    def add_subparsers(self, **kwargs):
        parser_class = kwargs.get("parser_class", type(self))
        if issubclass(parser_class, CommandParser):
            kwargs["parser_class"] = partial(
                parser_class,
                called_from_command_line=self.called_from_command_line,
            )
        return super().add_subparsers(**kwargs)


class DjangoHelpFormatter(HelpFormatter):
    """
    Customized formatter so that command-specific arguments appear in the
    --help output before arguments common to all commands.
    """

    show_last = {
        "--version",
        "--verbosity",
        "--traceback",
        "--settings",
        "--pythonpath",
        "--no-color",
        "--force-color",
        "--skip-checks",
    }

    def _reordered_actions(self, actions):
        return sorted(
            actions, key=lambda a: set(a.option_strings) & self.show_last != set()
        )

    def add_usage(self, usage, actions, *args, **kwargs):
        super().add_usage(usage, self._reordered_actions(actions), *args, **kwargs)

    def add_arguments(self, actions):
        super().add_arguments(self._reordered_actions(actions))


class OutputWrapper(TextIOBase):
    """
    Wrapper around stdout/stderr
    """

    @property
    def style_func(self):
        return self._style_func

    @style_func.setter
    def style_func(self, style_func):
        if style_func and self.isatty():
            self._style_func = style_func
        else:
            self._style_func = lambda x: x

    def __init__(self, out, ending="\n"):
        self._out = out
        self.style_func = None
        self.ending = ending

    def __getattr__(self, name):
        return getattr(self._out, name)

    def flush(self):
        if hasattr(self._out, "flush"):
            self._out.flush()

    def isatty(self):
        return hasattr(self._out, "isatty") and self._out.isatty()

    def write(self, msg="", style_func=None, ending=None):
        ending = self.ending if ending is None else ending
        if ending and not msg.endswith(ending):
            msg += ending
        style_func = style_func or self.style_func
        self._out.write(style_func(msg))


class BaseCommand:
    # Metadata about this command.
    help = ""

    # Configuration shortcuts that alter various logic.
    _called_from_command_line = False
    output_transaction = False  # Whether to wrap the output in a "BEGIN; COMMIT;"
    requires_system_checks = "__all__"
    # Arguments, common to all commands, which aren't defined by the argument
    # parser.
    base_stealth_options = ("stderr", "stdout")
    # Command-specific options not defined by the argument parser.
    stealth_options = ()
    suppressed_base_arguments = set()

    name = None
    status = CommandStatus.AVAILABLE

    cache_file = os.path.join(CONFIG_PATH, "command_cache")

    @property
    def config_path(self):
        path = os.path.join(CONFIG_PATH, self.command_name)
        if not os.path.exists(path):
            os.makedirs(path)
        return path

    @classproperty
    def command_name(cls) -> str:
        return cls.name or cls.__module__.split(".")[-1]

    @command_name.setter
    def command_name(cls, value):
        cls.name = value

    def __init__(self, stdout=None, stderr=None, no_color=False, force_color=False):
        self.stdout = OutputWrapper(stdout or sys.stdout)
        self.stderr = OutputWrapper(stderr or sys.stderr)
        self.proxies = None
        if no_color and force_color:
            raise CommandError("'no_color' and 'force_color' can't be used together.")
        if no_color:
            self.style = no_style()
        else:
            self.style = color_style(force_color)
            self.stderr.style_func = self.style.ERROR
        if (
            not isinstance(self.requires_system_checks, (list, tuple))
            and self.requires_system_checks != ALL_CHECKS
        ):
            raise TypeError("requires_system_checks must be a list or tuple.")

    def create_parser(self, prog_name, subcommand, **kwargs):
        """
        Create and return the ``ArgumentParser`` which will be used to
        parse the arguments to this command.
        """
        kwargs.setdefault("formatter_class", DjangoHelpFormatter)
        parser = CommandParser(
            prog="%s %s" % (os.path.basename(prog_name), subcommand),
            description=self.help or None,
            missing_args_message=getattr(self, "missing_args_message", None),
            called_from_command_line=getattr(self, "_called_from_command_line", None),
            **kwargs,
        )
        self.add_base_argument(
            parser,
            "-v",
            "--verbosity",
            default=1,
            type=int,
            choices=[0, 1, 2, 3],
            help=(
                "Verbosity level; 0=minimal output, 1=normal output, 2=verbose output, "
                "3=very verbose output"
            ),
        )
        self.add_base_argument(
            parser,
            "--pythonpath",
            help=(
                "A directory to add to the Python path, e.g. "
                '"/home/djangoprojects/myproject".'
            ),
        )
        self.add_base_argument(
            parser,
            "--traceback",
            action="store_true",
            help="Raise on CommandError exceptions.",
        )
        self.add_base_argument(
            parser,
            "--no-color",
            action="store_true",
            help="Don't colorize the command output.",
        )
        self.add_base_argument(
            parser,
            "--force-color",
            action="store_true",
            help="Force colorization of the command output.",
        )
        self.add_base_argument(
            parser,
            '--proxy',
            help='default proxy is None, specify system to use system proxy, or specify a proxy url',
        )
        self.add_base_argument(
            parser,
            '--cache',
            action='store_true',
            help='Using last cache to run command, default is False',
        )
        if self.requires_system_checks:
            parser.add_argument(
                "--skip-checks",
                action="store_true",
                help="Skip system checks.",
            )
        self.add_arguments(parser)
        return parser

    def add_arguments(self, parser: CommandParser):
        """
        Entry point for subclassed commands to add custom arguments.
        """
        pass

    def add_base_argument(self, parser, *args, **kwargs):
        """
        Call the parser's add_argument() method, suppressing the help text
        according to BaseCommand.suppressed_base_arguments.
        """
        for arg in args:
            if arg in self.suppressed_base_arguments:
                kwargs["help"] = argparse.SUPPRESS
                break
        parser.add_argument(*args, **kwargs)

    def print_help(self, prog_name, subcommand):
        """
        Print the help message for this command, derived from
        ``self.usage()``.
        """
        parser = self.create_parser(prog_name, subcommand)
        parser.print_help()

    def run_from_argv(self, argv):
        """
        Set up any environment changes requested (e.g., Python path
        and Django settings), then run this command. If the
        command raises a ``CommandError``, intercept it and print it sensibly
        to stderr. If the ``--traceback`` option is present or the raised
        ``Exception`` is not ``CommandError``, raise it.
        """
        self._called_from_command_line = True
        parser = self.create_parser(argv[0], argv[1])

        options = parser.parse_args(argv[2:])
        cmd_options = vars(options)
        # Move positional args out of options to mimic legacy optparse
        args = cmd_options.pop("args", ())
        try:
            self.execute(*args, **cmd_options)
        except CommandError as e:
            if options.traceback:
                raise

            # SystemCheckError takes care of its own formatting.
            if isinstance(e, SystemCheckError):
                self.stderr.write(str(e), lambda x: x)
            else:
                self.stderr.write("%s: %s" % (e.__class__.__name__, e))
            sys.exit(e.returncode)

    def execute(self, *args, **options):
        """
        Try to execute this command, performing system checks if needed (as
        controlled by the ``requires_system_checks`` attribute, except if
        force-skipped).
        """
        if options["force_color"] and options["no_color"]:
            raise CommandError(
                "The --no-color and --force-color options can't be used together."
            )
        if options["force_color"]:
            self.style = color_style(force_color=True)
        elif options["no_color"]:
            self.style = no_style()
            self.stderr.style_func = None
        if options.get("stdout"):
            self.stdout = OutputWrapper(options["stdout"])
        if options.get("stderr"):
            self.stderr = OutputWrapper(options["stderr"])

        proxy = options.get('proxy')
        if proxy == 'system':
            proxy = None
        elif proxy:
            if proxy.startswith('http'):
                proxy = {'http': proxy, 'https': proxy}
            else:
                proxy = {'http': 'http://' + proxy, 'https': 'http://' + proxy}
        else:
            proxy = {'http': None, 'https': None}
        self.proxies = proxy

        use_cache = options.get('cache')
        cache = {}
        command_cache = {}
        if use_cache and os.path.exists(self.cache_file):
            with open(self.cache_file, 'rb') as f:
                cache = json.load(f)
                command_cache = cache.setdefault(self.command_name, {})
        cache_args = command_cache.get('args', [])
        cache_options = command_cache.setdefault('options', {})
        for k, v in options.items():
            if k == 'cache':
                continue
            if v not in [None, ''] or k not in cache_options:
                cache_options[k] = v
        output = self.handle(*(args or cache_args), **cache_options)
        if use_cache:
            with open(self.cache_file, 'w') as f:
                json.dump(cache, f)
        if output:
            self.stdout.write(output)
        return output

    def handle(self, *args, **options):
        """
        The actual logic of the command. Subclasses must implement
        this method.
        """
        raise NotImplementedError(
            "subclasses of BaseCommand must provide a handle() method"
        )


class RemoteCommandManager(dict, BaseCommand):
    def __init__(self, servers: Union[List, None, str] = None):

        if not isinstance(servers, list):
            if servers is None:
                servers = os.environ.get('REMOTE_COMMAND_SERVERS', None)
            servers = [x.strip() for x in servers.split(',')] if servers else []
        self._current_server = None
        self._current_command = None
        for server in servers:
            self.register_server(server)
        self: Dict[str, Union[None, str, Dict[str, str]]]
        super().__init__()

    def __call__(self, command_name) -> 'RemoteCommandManager':
        for server, commands in self.items():
            if isinstance(commands, dict) and command_name in commands:
                self._current_server = server
                self._current_command = command_name
                return self
        raise KeyError("Command %s not found" % command_name)

    @property
    def current_command(self):
        return self[self._current_server][self._current_command]

    def run_from_argv(self, argv):
        parser = self.create_parser(argv[0], argv[1])
        options = parser.parse_args(argv[2:])
        cmd_options = vars(options)
        # Move positional args out of options to mimic legacy optparse
        args = cmd_options.pop("args", ())
        try:
            self.execute(server=self._current_server, command=self._current_command, **cmd_options)
        except CommandError as e:
            if options.traceback:
                raise
            sys.exit(e.returncode)

    def add_arguments(self, parser: CommandParser):
        properties = self.current_command['scheme']['properties']
        for key, detail in properties['kwargs']['properties'].items():
            parser.add_argument(
                '--%s' % key,
                # type=detail['type'],
                required=detail.get('required', False),
                default=detail.get('default', None),
            )

    def handle(self, *args, server=None, command=None, **options):
        kwargs = self.current_command['scheme']['properties']['kwargs']['properties']
        try:
            url = urljoin(server, 'execute/')
            response = requests.get(url, params={
                "name": command,
                "kwargs": json.dumps({k: options[k] for k in kwargs}),
            })
            content = response.json()
            if content['status'] == 'success':
                print(content['result'])
            else:
                raise CommandError(content['message'])
        except Exception as e:
            raise RuntimeError("Failed to execute command %s from %s: %s" % (command, server, e))
        finally:
            self._current_server = None
            self._current_command = None

    def register_server(self, server):
        assert re.match(r'^https?:/{2}\w.+$', server), "Invalid server URL"
        self[server] = None

    def load_from_server(self, server):
        try:
            response = requests.get(urljoin(server, 'list/'))
            assert response.status_code == 200, "list commands failed, response is %s" % response.text
        except Exception as e:
            self[server] = str(e)
            raise ImportError("Failed to load commands from %s: %s" % (server, e))
        self[server] = {x['name']: x for x in response.json()['commands']}

    def _ensure_loaded(self):
        for server, commands in super().items():
            if commands is None:
                self.load_from_server(server)

    def __getitem__(self, key):
        self._ensure_loaded()
        return super(RemoteCommandManager, self).__getitem__(key)

    def __len__(self):
        self._ensure_loaded()
        return super(RemoteCommandManager, self).__len__()

    def __contains__(self, item):
        self._ensure_loaded()
        return super(RemoteCommandManager, self).__contains__(item)

    def __iter__(self):
        self._ensure_loaded()
        return super(RemoteCommandManager, self).__iter__()

    def keys(self):
        self._ensure_loaded()
        return super(RemoteCommandManager, self).keys()

    def values(self):
        self._ensure_loaded()
        return super(RemoteCommandManager, self).values()

    def items(self):
        self._ensure_loaded()
        return super(RemoteCommandManager, self).items()

    def find(self, name):
        return self[name]

    def __str__(self):
        return "RemoteCommandManager(path=%s, num=%s)" % (self.keys(), len(self))


RemoteCommand = RemoteCommandManager()

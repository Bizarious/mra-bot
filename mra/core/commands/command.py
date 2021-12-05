from typing import Callable
from .context import Context
from .errors import CommandDoesNotExistError
from core.ext import ExtensionHandlerFeature, ExtensionFeature


def command(alias: str = None):
    def decorator(func: Callable):
        if alias is None:
            return Command(func, func.__name__)
        return Command(func, alias)
    return decorator


def group(alias: str = None):
    def decorator(func: Callable):
        if alias is None:
            return CommandGroup(func, func.__name__)
        return CommandGroup(func, alias)
    return decorator


class Command:
    """
    The command class.
    """

    def __init__(self, func: Callable, name: str):
        self.__func = func
        self.__name = name

    def __call__(self, *args, **kwargs):
        return self.__func(*args, **kwargs)

    @property
    def name(self):
        return self.__name


class CommandGroup(Command):
    """
    A group containing subcommands.
    """

    def __init__(self, func: Callable, name: str):
        Command.__init__(self, func, name)
        self._commands = {}

    def __call__(self, *args, **kwargs):
        if len(args) > 2 and args[2] in self._commands:
            extension = args[0]
            context = args[1]
            sub_command_name = args[2]
            args = args[3:]

            command_func = self._commands[sub_command_name]
            return command_func(extension, context, *args, **kwargs)

        return Command.__call__(self, *args, **kwargs)

    @property
    def commands(self):
        return self._commands

    def command(self, alias: str = None):
        """
        Decorator for adding a command to the group.
        """
        def decorator(func: Callable):
            if alias is None:
                self._commands[func.__name__] = Command(func, func.__name__)
            self._commands[alias] = Command(func, alias)
        return decorator


class ExtensionCommandFeature(ExtensionFeature):

    def __init__(self):
        self._commands = {}

    @property
    def commands(self):
        return self._commands

    def add_command(self, name: str, cmd: Command):
        self._commands[name] = cmd


class HandlerCommandFeature(ExtensionHandlerFeature):
    """
    Mixin part for command handling.
    """

    def __init__(self, types, to_be_executed: [Callable]):
        ExtensionHandlerFeature.__init__(self, types, "Command", "CommandGroup")
        self._commands = {}
        to_be_executed.append(self._add_commands)

    @property
    def commands(self) -> dict:
        return self._commands

    def _add_command(self, name: str, cmd: Command, extension: ExtensionCommandFeature) -> None:
        if name in self._commands:
            raise RuntimeError(f'The command "{name}" already exists')
        self._commands[name] = {
            "command": cmd,
            "extension": extension
        }
        extension.add_command(name, cmd)

    def _add_commands(self, attributes: dict, extension: ExtensionCommandFeature) -> None:
        for cmd in attributes["Command"]:
            self._add_command(cmd.name, cmd, extension)
        for cmd_group in attributes["CommandGroup"]:
            self._add_command(cmd_group.name, cmd_group, extension)

    def handle_command(self, context: Context, command_prefix: str) -> None:
        """
        Handles incoming command requests.
        """
        cmd = context.command
        if not cmd.startswith(command_prefix):
            return

        # replaces the prefix with an empty string, so we have the raw command word
        cmd = cmd.replace(command_prefix, "", 1)

        if cmd not in self._commands:
            raise CommandDoesNotExistError(f'The command "{cmd}" does not exist')

        command_func = self._commands[cmd]["command"]
        extension = self._commands[cmd]["extension"]
        arguments = context.arguments

        command_func(extension, context, *arguments)

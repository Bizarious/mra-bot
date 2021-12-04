from typing import Callable
from .context import Context
from .errors import CommandDoesNotExistError
from core.ext import ExtensionHandlerFeature, Extension, ExtensionFeature


def command(alias: str = None):
    def decorator(func: Callable):
        if alias is None:
            return Command(func, func.__name__)
        return Command(func, alias)
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


class HandlerCommandFeature(ExtensionHandlerFeature):
    """
    Mixin part for command handling.
    """

    def __init__(self, types, to_be_executed: [Callable]):
        ExtensionHandlerFeature.__init__(self, types, "Command")
        self._commands = {}
        to_be_executed.append(self._add_commands)

    def _add_command(self, name: str, cmd: Command, extension: Extension) -> None:
        if name in self._commands:
            raise RuntimeError(f'The command "{name}" already exists')
        self._commands[name] = {
            "command": cmd,
            "extension": extension
        }

    def _add_commands(self, attributes: dict, extension: Extension) -> None:
        for cmd in attributes["Command"]:
            self._add_command(cmd.name, cmd, extension)

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


class ExtensionCommandFeature(ExtensionFeature):
    pass

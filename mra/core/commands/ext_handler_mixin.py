from typing import Callable
from .command import Command
from .errors import CommandDoesNotExistError
from .context import Context
from core.ext import Extension, ExtensionHandlerFeature


class CommandFeature(ExtensionHandlerFeature):
    """
    Mixin part for command handling.
    """

    def __init__(self, types, to_be_executed: [Callable]):
        ExtensionHandlerFeature.__init__(self, types, "Command")
        self._commands = {}
        to_be_executed.append(self._add_commands)

    def _add_command(self, name: str, command: Command, extension: Extension) -> None:
        if name in self._commands:
            raise RuntimeError(f'The command "{name}" already exists')
        self._commands[name] = {
            "command": command,
            "extension": extension
        }

    def _add_commands(self, attributes: dict, extension: Extension) -> None:
        for command in attributes["Command"]:
            self._add_command(command.name, command, extension)

    def handle_command(self, context: Context, command_prefix: str) -> None:
        """
        Handles incoming command requests.
        """
        command = context.command
        if not command.startswith(command_prefix):
            return

        # replaces the prefix with an empty string, so we have the raw command word
        command = command.replace(command_prefix, "", 1)

        if command not in self._commands:
            raise CommandDoesNotExistError(f'The command "{command}" does not exist')

        command_func = self._commands[command]["command"]
        extension = self._commands[command]["extension"]
        arguments = context.arguments

        command_func(extension, context, *arguments)





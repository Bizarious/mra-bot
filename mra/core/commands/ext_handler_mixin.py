from typing import Callable
from .command import Command
from core.ext import Extension, ExtensionHandlerFeature


class CommandFeature(ExtensionHandlerFeature):
    """
    Mixin part for command handling.
    """

    def __init__(self, types):
        ExtensionHandlerFeature.__init__(self, types, "Command")
        self._commands = {}

    def _add_command(self, name: str, command: Command, extension: Extension) -> None:
        if name in self._commands:
            raise RuntimeError(f'The command "{name}" already exists')
        self._commands[name] = {
            "command": command,
            "extension": extension
        }

    def _add_commands(self, command_list: [Command], extension: Extension) -> None:
        for command in command_list:
            self._add_command(command.name, command, extension)


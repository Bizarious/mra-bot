from .ext_handler_mixin import CommandFeature
from core.ext import ExtensionInterface


class CommandInterface(ExtensionInterface):
    """
    An interface used to provide command extensions an controllable
    set of functionality.
    """
    def __init__(self, bot):
        ExtensionInterface.__init__(self, bot)
        self._bot = self._entity

    @property
    def extension_handler(self) -> CommandFeature:
        return self._bot.extension_handler

    def stop_bot(self):
        self._bot.stop()

from .command import HandlerCommandFeature, ExtensionCommandFeature
from core.ext import ExtensionHandler, Extension, ExtensionInterface


class BotExtensionHandler(ExtensionHandler, HandlerCommandFeature):

    def __init__(self, interface, *paths: str):
        ExtensionHandler.__init__(self, interface, *paths)

        HandlerCommandFeature.__init__(self, self._accessible_types,
                                       self._to_be_executed_on_extension_loading
                                       )


class BotInterface(ExtensionInterface):
    """
    An interface used to provide command extensions an controllable
    set of functionality.
    """
    def __init__(self, bot):
        self._bot = bot

    @property
    def extension_handler(self) -> ExtensionCommandFeature:
        return self._bot.extension_handler

    def stop_bot(self):
        self._bot.stop()

    def restart_bot(self):
        self._bot.restart()


class BotExtension(Extension, ExtensionCommandFeature):

    def __init__(self, interface: BotInterface):
        Extension.__init__(self, interface)

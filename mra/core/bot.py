from .api_layer import APILayer, APICommandAdapter
from core.commands import CommandFeature
from core.ext import ExtensionHandler


class BotExtensionHandler(ExtensionHandler, CommandFeature):

    def __init__(self, *paths: str):
        ExtensionHandler.__init__(self, *paths)

        CommandFeature.__init__(self, self._accessible_types,
                                self._to_be_executed_on_extension_loading
                                )


class Bot:
    """
    The main class of the application.
    """

    def __init__(self, api_layer: APILayer):
        # the api layer, implemented by the used platform
        self.__api_layer = api_layer

        # the extension layer, used to process commands, listeners etc.
        self.__extension_handler = BotExtensionHandler("core/extensions")

        # an adapter to allow communication between command interface and api
        self.__api_command_adapter = APICommandAdapter(self.__api_layer, self.__extension_handler)

    def test(self):
        self.__extension_handler.load_extensions_from_paths()
        self.__extension_handler.load_extension("System")

    def run(self):
        self.__api_layer.add_message_handler(self.__api_command_adapter.translate)
        self.__api_layer.run()


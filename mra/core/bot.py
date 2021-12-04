from .api_layer import APILayer, APICommandAdapter
from core.commands import BotInterface, BotExtensionHandler
import os
import sys


class Bot:
    """
    The main class of the application.
    """

    def __init__(self, api_layer: APILayer):
        # the api layer, implemented by the used platform
        self.__api_layer = api_layer

        # the interface that is given to every extension
        self.__interface = BotInterface(self)

        # the extension layer, used to process commands, listeners etc.
        self.__extension_handler = BotExtensionHandler(self.__interface, "core/extensions")

        # an adapter to allow communication between command interface and api
        self.__api_command_adapter = APICommandAdapter(self.__api_layer, self.__extension_handler)

    @property
    def extension_handler(self):
        return self.__extension_handler

    def test(self):
        self.__extension_handler.load_extensions_from_paths()
        self.__extension_handler.load_extension("System")

    def run(self):
        self.__api_layer.add_message_handler(self.__api_command_adapter.translate)
        self.__api_layer.run()

    def stop(self):
        self.__api_layer.stop()

    def restart(self):
        self.stop()
        os.execv(sys.executable, [sys.executable.split("/")[-1]] + sys.argv)

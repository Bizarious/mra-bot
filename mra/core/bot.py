from core import APILayer
from core.commands import CommandFeature
from core.ext import ExtensionHandler


class BotExtensionHandler(ExtensionHandler, CommandFeature):

    def __init__(self, *paths: str):
        ExtensionHandler.__init__(self, *paths)
        CommandFeature.__init__(self, self._accessible_types)
        self._extensions = {}

    def load_extension(self, name: str) -> None:
        extension_class = self._extension_classes[name]
        extension = extension_class(name)
        attributes = self._loader.get_attributes(extension, self._accessible_types)
        self._add_commands(attributes["Command"], extension)
        self._extensions[name] = extension


class Bot:
    """
    The main class of the application.
    """

    def __init__(self, api_layer: APILayer):
        self.__api_layer = api_layer
        self.__extension_handler = BotExtensionHandler("core/extensions")

    def test(self, _):
        print("Message")

    def test2(self):
        self.__extension_handler.load_extensions_from_paths()
        self.__extension_handler.load_extension("System")

    def run(self):
        self.__api_layer.add_message_handler(self.test)
        self.__api_layer.run()


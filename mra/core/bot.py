from core import APILayer


class Bot:
    """
    The main class of the application.
    """

    def __init__(self, api_layer: APILayer):
        self.__api_layer = api_layer

    def test(self, _):
        print("Message")

    def run(self):
        self.__api_layer.add_message_handler(self.test)
        self.__api_layer.run()


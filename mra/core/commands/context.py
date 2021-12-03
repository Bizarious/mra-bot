class Context:

    def __init__(self,
                 api_layer,
                 message: str,
                 chat_id: int,
                 message_id: int
                 ):

        self.__api_layer = api_layer  # no type because of circular imports

        self.__message = message
        self.__command, self.__arguments = self.__split_command_and_args()
        self.__chat_id = chat_id
        self.__message_id = message_id

    def __split_command_and_args(self) -> tuple:
        message = self.__message.split(" ")
        command = message[0]
        arguments = message[1:]
        return command, arguments

    @property
    def message(self) -> str:
        return self.__message

    @property
    def command(self) -> str:
        return self.__command

    @property
    def arguments(self) -> list:
        return self.__arguments

    @property
    def chat_id(self) -> int:
        return self.__chat_id

    @property
    def message_id(self) -> int:
        return self.__message_id

    def send(self, message: str) -> None:
        self.__api_layer.send_message(self.chat_id, message)

    def reply(self, message: str) -> None:
        self.__api_layer.reply_to_message(self.chat_id, message, self.message_id)

import telebot
from typing import Callable
from core import APILayer
from core.commands import Context
from tele_token import __token__


class TelegramAPI(APILayer):

    def __init__(self):
        APILayer.__init__(self, prefix="/")
        self.bot = telebot.TeleBot(__token__, threaded=False, skip_pending=True)
        telebot.apihelper.SESSION_TIME_TO_LIVE = 5 * 60

    def run(self) -> None:
        self.bot.infinity_polling()

    def add_message_handler(self, cmd: Callable) -> None:
        self.bot.message_handler(func=lambda m: True)(cmd)

    def create_context(self, message: telebot.types.Message) -> Context:
        context = Context(
            api_layer=self,
            message=message.text,
            chat_id=message.chat.id,
            message_id=message.message_id
        )
        return context

    def send_message(self, chat_id: int, message: str) -> None:
        self.bot.send_message(chat_id, message)

    def reply_to_message(self, chat_id: int, message: str, message_id: int) -> None:
        self.bot.send_message(chat_id, message, reply_to_message_id=message_id)

    def stop(self) -> None:
        self.bot.stop_polling()
        self.bot.get_updates(offset=self.bot.last_update_id+1, long_polling_timeout=1)

    def on_command_error(self, ctx: Context, exception: Exception) -> None:
        raise NotImplementedError()

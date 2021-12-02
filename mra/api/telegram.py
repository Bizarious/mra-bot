import telebot
from typing import Callable
from core import APILayer
from tele_token import __token__


class TelegramAPI(APILayer):

    def __init__(self):
        self.bot = telebot.TeleBot(__token__, threaded=True)
        telebot.apihelper.SESSION_TIME_TO_LIVE = 5 * 60

    def run(self) -> None:
        self.bot.infinity_polling()

    def add_message_handler(self, cmd: Callable) -> None:
        self.bot.message_handler(func=lambda m: True)(cmd)

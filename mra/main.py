from core import Bot
from api.telegram import TelegramAPI

b = Bot(TelegramAPI())
b.test()
b.run()

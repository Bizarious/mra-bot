import telebot
import time
import threading


class T(threading.Thread):

	def __init__(self, tb, cid):
		threading.Thread.__init__(self)
		self.tb: telebot.TeleBot = tb
		self.cid = cid

	def run(self):
		time.sleep(3)
		self.tb.send_message(self.cid, "Test")


class Bot:

	def __init__(self, b):
		self.b: telebot.TeleBot = b
		self.b.message_handler(func=lambda message: True)(self.test)

	def test(self, message):
		self.b.send_message(message.chat.id, "Test")


bot = telebot.TeleBot("2080135094:AAHLs4LbKbNqr_MFbr7cuPEoxiExBpHAgJM", threaded=True)
stop = False

telebot.apihelper.SESSION_TIME_TO_LIVE = 5 * 60


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	t = T(bot, message.chat.id)
	t.start()


@bot.message_handler(commands=["test"])
def test(message):
	bot.send_message(message.chat.id, "Test")


def stop_it(_):
	bot.stop_bot()


bot.message_handler(commands=["stop"])(stop_it)


#@bot.message_handler(func=lambda message: True)
def echo_all(message):
	print(dir(message))
	print(dir(message.from_user))
	print(message.from_user)


bot2 = Bot(bot)


u = bot.get_updates(timeout=2)

if u:
	bot.get_updates(offset=u[-1].update_id+1)

bot.infinity_polling()

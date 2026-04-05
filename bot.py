import threading

import telebot

from config import BOT_TOKEN
from handlers.start import auto_send
from services_bot.logger_func import setup_logger
from services_bot.time_zone import time_thread

bot = telebot.TeleBot(BOT_TOKEN)


logger = setup_logger("bot_logger")
logger.info("Начало работы бота")

start_thread = threading.Thread(target=auto_send, args=(bot,))

start_thread.start()
time_thread.start()


if __name__ == "__main__":
    print("Бот запущен...")
    bot.polling(non_stop=True)

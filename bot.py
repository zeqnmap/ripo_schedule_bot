import threading

import telebot

from config import BOT_TOKEN
from handlers.start import auto_send
from handlers.help import register_help_handler
from services_bot.logger_func import setup_logger
from services_bot.time_zone import time_thread
from handlers.commands import set_bot_commands
from handlers.last_schedule import register_last_schedule_handler


bot = telebot.TeleBot(BOT_TOKEN)


logger = setup_logger("bot_logger")
logger.info("Начало работы бота")

start_thread = threading.Thread(target=auto_send, args=(bot,))


if __name__ == "__main__":
    set_bot_commands(bot)
    register_help_handler(bot)
    register_last_schedule_handler(bot)

    start_thread.start()
    time_thread.start()

    print("Бот запущен...")
    bot.polling(non_stop=True)

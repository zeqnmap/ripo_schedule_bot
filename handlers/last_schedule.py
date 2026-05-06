import os
import telebot
from config import FOLDER_PATH
from services_bot.logger_func import setup_logger

logger = setup_logger("last_schedule")


def register_last_schedule_handler(bot: telebot.TeleBot):
    @bot.message_handler(commands=['schedule'])
    def send_latest_schedule(message):
        logger.info(f"Пользователь {message.chat.id} запросил последнее расписание")

        if not os.path.exists(FOLDER_PATH):
            bot.reply_to(message, "📁 Папка с расписанием не найдена.")
            logger.error(f"Папка не существует: {FOLDER_PATH}")
            return

        files = [
            f for f in os.listdir(FOLDER_PATH)
            if os.path.isfile(os.path.join(FOLDER_PATH, f))
               and f.lower().endswith(('.pdf',))
        ]

        if not files:
            bot.reply_to(message, "📭 Нет файлов расписания в папке.")
            logger.warning("Нет файлов в папке расписания")
            return

        file_paths = [os.path.join(FOLDER_PATH, f) for f in files]
        latest_file = max(file_paths, key=os.path.getmtime)

        try:
            with open(latest_file, 'rb') as document:
                bot.send_document(
                    message.chat.id,
                    document,
                    caption="📌 Последнее расписание"
                )
            logger.info(f"Отправлен файл: {latest_file}")
        except Exception as e:
            bot.reply_to(message, "❌ Не удалось отправить файл.")
            logger.error(f"Ошибка при отправке файла {latest_file}: {e}")
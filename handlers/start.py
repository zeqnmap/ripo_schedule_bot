import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import sqlite3
import time
from services_bot.take_user_id import take_users_id
from services_bot.file_size_control import FLAG, take_new_file
from services_bot.logger_func import setup_logger
from config import DB_PATH


logger = setup_logger('auto_start')


def auto_send(bot):
    @bot.message_handler(commands=['start'])
    def send_welcome(message):
        user_id = message.chat.id
        username = message.from_user.username

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR IGNORE INTO users (user_id, username)
            VALUES (?, ?)
        ''', (user_id, username))
        conn.commit()
        conn.close()
        bot.reply_to(message, "Добро пожаловать! Здесь будет появляться новое расписание — не отключай уведомления ;)")

    while True:
        current_file = take_new_file()

        if FLAG['FLAG']:
            logger.info("FLAG == True --> начинаем рассылку ")
            for user_ids in take_users_id():
                try:
                    with open(current_file, 'rb') as file:
                        logger.info('открыли файлы')
                        bot.send_document(
                            chat_id=user_ids,
                            document=file,
                            caption=f"📅 Новое расписание"
                        )

                        time.sleep(0.1)

                except Exception as e:
                    logger.error(f"Ошибка отправки {user_ids}: {e}")
            logger.info("Рассылка завершена")
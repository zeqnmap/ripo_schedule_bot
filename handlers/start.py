from services_bot.database import db
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import time
from services_bot.file_size_control import FLAG, take_new_file
from services_bot.logger_func import setup_logger

logger = setup_logger("auto_start")


def auto_send(bot):
    @bot.message_handler(commands=["start"])
    def send_welcome(message):
        user_id = message.chat.id
        username = message.from_user.username or "unknown"

        if db.user_exists(user_id):
            db.update_username(user_id, username)

            bot.reply_to(
                message,
                "👋 Добро пожаловать! \n\n✅Здесь будет появляться новое расписание — не отключай уведомления ;)\n\n"
                "‼️Переходи в канал колледжа, чтобы не пропустить важные события: @kstmia_uo_ripo"
            )
        else:
            db.add_user(user_id, username)

            bot.reply_to(
                message,
                "👋 Добро пожаловать! \n\n✅Здесь будет появляться новое расписание — не отключай уведомления ;)\n\n"
                "‼️Переходи в канал колледжа, чтобы не пропустить важные события: @kstmia_uo_ripo"
            )

            try:
                with open("handlers/schedule.png", "rb") as photo:
                    bot.send_photo(
                        chat_id=user_id,
                        photo=photo,
                        caption="📌 Если нужно расписание — закрепи это сообщение!"
                    )
            except FileNotFoundError:
                logger.error("ERROR файл schedule.png отсутствует")

    while True:
        current_file = take_new_file()

        if FLAG["FLAG"]:
            logger.info("FLAG == True --> начинаем рассылку")
            for user_id_ in db.get_all_user_ids():
                try:
                    with open(current_file, "rb") as file:
                        bot.send_document(
                            chat_id=user_id_,
                            document=file,
                            caption="📅 Новое расписание"
                        )
                        time.sleep(0.1)
                except Exception as e:
                    logger.error(f"Ошибка отправки {user_id_}: {e}")
            logger.info("Рассылка завершена")
import sqlite3
import telebot
from config import BOT_TOKEN, DB_PATH


bot = telebot.TeleBot(BOT_TOKEN)


def broadcast_to_all(message_text=None, photo_path=None, caption=None):
    """
    Рассылает сообщение или фото всем пользователям из БД

    :param message_text: Текст сообщения
    :param photo_path: Путь к фото
    :param caption: Подпись к фото
    """
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()

            cursor.execute("SELECT user_id FROM users")
            users = cursor.fetchall()

        if not users:
            print("Нет пользователей в БД")
            return

        print(f"Начинаю рассылку для {len(users)} пользователей...")

        success_count = 0
        fail_count = 0

        for (user_id,) in users:
            try:
                if photo_path:
                    with open(photo_path, 'rb') as photo:
                        bot.send_photo(user_id, photo, caption=caption or message_text)
                else:
                    bot.send_message(user_id, message_text)

                success_count += 1

            except Exception as e:
                print(f"Ошибка отправки пользователю {user_id}: {e}")
                fail_count += 1

            import time
            time.sleep(0.1)

        print(f"Рассылка завершена: {success_count} успешно, {fail_count} ошибок")

    except Exception as e:
        print(f"Критическая ошибка рассылки: {e}")


if __name__ == '__main__':
    # broadcast_to_all(message_text="Важное объявление")

    broadcast_to_all(
        photo_path="/Users/yaroslavmanko/PycharmProjects/ripo_schedule_bot/IMG_1177.JPG", # путь к фотке, которую нужно отправить
        caption="Кому нужно — закрепите."
    )
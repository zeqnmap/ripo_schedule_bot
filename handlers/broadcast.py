import telebot

from config import BOT_TOKEN
from services_bot.database import db


bot = telebot.TeleBot(BOT_TOKEN)


def broadcast_to_all(message_text=None, photo_path=None, caption=None):
    """
    Рассылает сообщение или фото всем пользователям из БД

    :param message_text: Текст сообщения
    :param photo_path: Путь к фото
    :param caption: Подпись к фото
    """
    user_ids = db.get_all_user_ids()

    if not user_ids:
        print("❌ Нет пользователей в БД для рассылки")
        return

    print(f"🚀 Начинаю рассылку для {len(user_ids)} пользователей...")

    success_count = 0
    blocked_count = 0
    error_count = 0

    for user_id in user_ids:
        try:
            if photo_path:
                with open(photo_path, "rb") as photo:
                    bot.send_photo(
                        chat_id=user_id,
                        photo=photo,
                        caption=caption
                    )
            elif message_text:
                bot.send_message(
                    chat_id=user_id,
                    text=message_text
                )
            success_count += 1

        except Exception as e:
            error_msg = str(e).lower()
            if "bot_blocked" in error_msg or "chat not found" in error_msg or "user is deactivated" in error_msg:
                blocked_count += 1
                print(f"⛔ Пользователь {user_id} заблокировал бота или неактивен")
            else:
                error_count += 1
                print(f"❌ Ошибка при отправке {user_id}: {e}")

    print(f"✅ Рассылка завершена: {success_count} доставлено, {blocked_count} заблокировано/неактивно, {error_count} других ошибок")
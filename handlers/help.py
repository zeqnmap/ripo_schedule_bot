import telebot


def register_help_handler(bot: telebot.TeleBot):
    @bot.message_handler(commands=['help'])
    def help_message(message):
        text = (
            "ℹ️ Если вам не пришло новое расписание, нажмите на кнопку /start в этом же меню, после чего на <<Последнее расписание>>\n\n"
            "Если проблема осталась — опишите её разработчику бота: @zeqnmap\n\n"
            "📬 Постараемся быстро решить вашу проблему!"
        )
        bot.reply_to(message, text)
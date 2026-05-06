import telebot


def set_bot_commands(bot):
    commands = [
        telebot.types.BotCommand("/start", "Запустить бота"),
        telebot.types.BotCommand("/help", "Помощь"),
        telebot.types.BotCommand("/schedule", "Последнее расписание"),
    ]
    bot.set_my_commands(commands)

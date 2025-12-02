from telegram_bot import bot
from handlers import *


if __name__ == "__main__":
    print("Бот запущен...")
    bot.infinity_polling()
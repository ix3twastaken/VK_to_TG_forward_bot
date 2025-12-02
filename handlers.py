from telegram_bot import bot, send_photo
from vk_api import get_photo_urls_from_vk_post


@bot.message_handler(commands=['last'])
def send_last_post(message):
    urls = get_photo_urls_from_vk_post(2)
    send_photo(urls)


@bot.message_handler(commands=['other'])
def ask_for_post_number(message):
    bot.send_message(message.chat.id, "Укажите номер поста (от 1 до 99):")

    @bot.message_handler(func=lambda msg: msg.text.isdigit() and 1 <= int(msg.text) <= 99)
    def send_chosen_post(message):
        count = message.text
        count = int(count)+1
        urls = get_photo_urls_from_vk_post(count)
        send_photo(urls)
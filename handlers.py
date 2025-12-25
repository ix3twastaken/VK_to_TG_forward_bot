from telegram_bot import bot, send_photo
from vk_api import get_new_urls
from vk_api import get_photo_urls_from_vk_post
from db.models import *

@bot.message_handler(commands=['new'])
def send_all_new_posts(message):
    # new_urls = get_photo_urls_from_vk_post(5)
    # send_photo(new_urls)

    new_urls, indxErr = get_new_urls()
    if indxErr == True:
        bot.send_message(message.chat.id, "Нет новых постов")
    else:
        send_photo(new_urls)
    print(new_urls)

@bot.message_handler(commands=['connect'])
def connect_to_db(message):
    urls = get_photo_urls_from_vk_post(99) 
    print(urls)
    last_url = urls[-1]
    add_last_url_to_db(1, last_url)

    print(last_url)
    print(last_url_db()[0])

@bot.message_handler(commands=['check'])
def db_check(message):
    bot.send_message(message.chat.id, f'{last_url_db()}')


# @bot.message_handler(commands=['other'])
# def ask_for_post_number(message):
#     bot.send_message(message.chat.id, "Укажите номер поста (от 1 до 99):")

#     @bot.message_handler(func=lambda msg: msg.text.isdigit() and 1 <= int(msg.text) <= 99)
#     def send_chosen_post(message):
#         count = message.text
#         count = int(count)+1
#         urls = get_photo_urls_from_vk_post(count)
#         send_photo(urls)
from telegram_bot import *
from vk_api import get_new_urls
from vk_api import get_photo_urls_from_vk_post
from db.models import add_last_url_to_db

@bot.message_handler(commands=['new'])
def send_all_new_posts(message):
    """
    Отправляет все новые посты
    """
    new_urls, indexErr = get_new_urls()
    if not indexErr:
        bot.send_message(message.chat.id, "Отправка изображений...")
    if indexErr:
        bot.send_message(message.chat.id, "Нет новых постов")
    else:
        send_post(new_urls, message)

@bot.message_handler(commands=['connect'])
def connect_to_db(message):
    """
    Меняет значение в базе данных на последнее изображение из поста post_index
    """
    post_index = 10 # Допустимые значения: (2, 99); Десятый пост стоит для того, чтобы проверить работоспособность бота
    urls = get_photo_urls_from_vk_post(post_index) 
    last_url = urls[-1]
    add_last_url_to_db(1, last_url)
    db_check(message)

# @bot.message_handler(commands=['other'])
# def ask_for_post_number(message):
#     bot.send_message(message.chat.id, "Укажите номер поста (от 1 до 99):")

#     @bot.message_handler(func=lambda msg: msg.text.isdigit() and 1 <= int(msg.text) <= 99)
#     def send_chosen_post(message):
#         count = message.text
#         count = int(count)+1
#         urls = get_photo_urls_from_vk_post(count)
#         send_photo(urls)
import telebot, time
from telebot import types
from config import BOT_API_TOKEN, CHAT_ID, MESSAGE_THREAD_ID


bot = telebot.TeleBot(BOT_API_TOKEN)


def send_photo(photo_urls):
    if not photo_urls:
        print("Нет фото для отправки")
        return

    if len(photo_urls) == 1:
        bot.send_photo(CHAT_ID, photo=photo_urls[0], message_thread_id=MESSAGE_THREAD_ID)
    else:
        media = [types.InputMediaPhoto(url) for url in photo_urls]
        bot.send_media_group(CHAT_ID, media, message_thread_id=MESSAGE_THREAD_ID)

def send_post(photo_urls):
    for post in photo_urls:
        send_photo(post)
        time.sleep(5)
import telebot, requests, json
from telebot import types
import access_tokens as at  # Импорт токенов (токен бота, сервисный ключ vk, айди конечного чата telegram)


API_TOKEN = at.BOT_API_TOKEN
bot = telebot.TeleBot(API_TOKEN)


def extract_urls(response_data, post_index):
    """
    Extracts photo URLs from a single VK post.
    response_data: dict - response from the VK API
    post_index: int - post index in the list of elements
    return list[str] - list of photo URLs
    """
    urls = []
    try:
        post = response_data["response"]["items"][post_index]
        attachments = post.get("attachments", [])
        for attachments in attachments:
            if attachments.get("type") == "photo":
                sizes = attachments.get("photo", {}).get("sizes", {})
                if sizes:
                    url = sizes[-1]["url"]
                    urls.append(url)
    except  (IndexError, KeyError) as e:
        print(f"Error extracting photo: {e}")
    return urls


# Получение обновлений изображения из VK
def get_updates(count):
    count = int(count)
    response = requests.get(
        f'https://api.vk.ru/method/wall.get',
        params={
            'domain': 'nyaslav',
            'count': count,
            'access_token': at.ACCESS_TOKEN,
            'v': '5.199'
        }
    )
    data = response.json()
    post_index = count - 1
    return extract_urls(data, post_index)

def send_image(count):
    CHAT_ID = '-100' + at.MY_CHAT_ID   # Конечный чат в которое отправляется сообщение (id = "-100" + "id чата")
    default_url = ''
    urls_list = get_updates(count)

    if urls_list == []:     # Проверка на случай, если тип данных не "photo"
        print("empty")
        pass
    else:
        if len(urls_list) < 2:  # Минимально допустимое значение массива, передеваемое в InputMediaPhoto равняется 2
            if default_url in urls_list:
                print("the same1")
                pass
            else: 
                default_url = urls_list[0]
                bot.send_photo(CHAT_ID, photo=default_url, message_thread_id=86031) #Для чата супергруппы 
                # bot.send_photo(CHAT_ID, photo=default_url) #Для обычной группы
        else:
            if default_url in urls_list: 
                print("the same2")
                pass
            else:
                bot.send_media_group(CHAT_ID, [types.InputMediaPhoto(i) for i in urls_list], message_thread_id=86031)
                # bot.send_media_group(CHAT_ID, [types.InputMediaPhoto(i) for i in urls_list]) #Для обычной группы

#Команда отправки сообщения
@bot.message_handler(commands=['last']) 
def send(msg):
    send_image(2)


@bot.message_handler(commands=['other'])
def change_count(message):
    bot.send_message(chat_id=message.chat.id, text=("Укажите номер от 2 до 100"))

    @bot.message_handler(func=lambda message: True)
    def send_count_image(message):
            count = message.text
            send_image(count)


if __name__ == "__main__":
    bot.infinity_polling()
import telebot, requests, json
from telebot import types
import access_tokens as at  # Импорт токенов (токен бота, сервисный ключ vk, айди конечного чата telegram)


API_TOKEN = at.BOT_API_TOKEN
bot = telebot.TeleBot(API_TOKEN)


# Получение обновлений изображения из VK
def get_updates(count):
    new_image_urls = []
    items_index = int(count) - 1
    
    image_url = requests.get(f'https://api.vk.ru/method/wall.get?domain=nyaslav&count={count}&access_token={at.ACCESS_TOKEN}&v=5.199') 
    json_urls = json.loads(image_url.text)
    photo_index = 0
    while photo_index < 10:
        try:
            if json_urls["response"]["items"][items_index]["attachments"][photo_index]["type"] == 'photo':    # Проверка на нужный тип файла
                urls = json_urls["response"]["items"][items_index]["attachments"][photo_index]["photo"]["sizes"][-1]["url"]    # Получение ссылки на изображение
                new_image_urls.append(urls)   # Добавление в список с ссылками для отправки
        except IndexError:
            print("index_error")
            pass

        photo_index += 1
    return new_image_urls

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
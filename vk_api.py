import requests
from access_tokens import ACCESS_TOKEN
from db.models import *

def get_photo_urls_from_vk_post(count) -> list:
    """
    Извлекает URL-адреса фотографий из одного поста VK.
    response_data: dict - ответ от VK API
    post_index: int - индекс поста в списке items
    return list[str] - список URL-адресов фото
    """
    count = int(count)
    post_index = count - 1
    response = requests.get(
        f'https://api.vk.ru/method/wall.get',
        params={
            'domain': 'nyaslav',
            'count': count,
            'access_token': ACCESS_TOKEN,
            'v': '5.199'
        }
    )
    data = response.json()

    urls = []
    try:
        post = data["response"]["items"][post_index]
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

def get_new_urls():
    """
    Просматривает все посты до тех пор, 
    пока не встретит последний уже отправленный в телеграм пост
    urls: list - список изображений из одного поста
    last_url: str - изображение из последнего отправленного поста
    new_urls: list - список новых изображений на отправку
    """
    post_index = 2 # Начинается с поста индексом 2
    last_url = last_url_db() # Получение последней отправленной ссылки из базы данных
    new_urls = []
    indexErr = False
    while True:
        try:
            urls = get_photo_urls_from_vk_post(post_index)
            if not urls:
                indexErr = save_last_url_in_db(new_urls)
                post_index+=1
                continue
            if urls[-1] == last_url:
                indexErr = save_last_url_in_db(new_urls)
                break
            
            new_urls.append(list(urls))
        except IndexError as e:
            indexErr = True
            print(f"Error extracting photo: {e}")
            break
        post_index+=1

    return new_urls, indexErr

def save_last_url_in_db(new_urls):
    indexErr = False
    if new_urls:
        latest_url = new_urls[0][0]
        add_last_url_to_db(1, latest_url)
    else:
        indexErr = True
        print("None")

    return indexErr

import requests
from access_tokens import ACCESS_TOKEN
from db.models import *

def get_photo_urls_from_vk_post(count) -> list:
    """
    Извлекает URL-адреса фотографий из одного поста VK.
    response_data: dict — ответ от VK API
    post_index: int — индекс поста в списке items
    return list[str] — список URL-адресов фото
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

def get_new_urls() -> list:
    """
    Просматривает все посты до тех пор, 
    пока не встретит последний уже отправленный в телеграм пост
    last_url: str - изображение из последнего отправленного поста
    new_urls: list - список новый изображение на отправку
    """
    i = 2
    last_url = last_url_db()[0] #получение последней ссылки из базы данных
    new_urls=[]
    indexErr = False
    while True:
        try:
            urls = get_photo_urls_from_vk_post(i)
            if urls == []:
                add_last_url_to_db(1, new_urls[-1])
                break
            elif urls[-1] != last_url:
                for url in urls:
                    new_urls.append(url)
            else:
                add_last_url_to_db(1, new_urls[-1])
                break
        except IndexError:
            indexErr = True
            print('list index out of range')
            break
        i+=1
    return new_urls, indexErr
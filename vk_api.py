import requests
from access_tokens import ACCESS_TOKEN

def get_photo_urls_from_vk_post(count):
    """
    Extracts photo URLs from a single VK post.
    response_data: dict - response from the VK API
    post_index: int - post index in the list of elements
    return list[str] - list of photo URLs
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
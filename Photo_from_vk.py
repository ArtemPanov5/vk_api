import vk_api
import time
from vk_api.exceptions import VkApiError

# https://vk.barkov.net/maildownload.aspx
# Initialize the VK session
vk_token = 'введите ваш личный токен'
vk_session = vk_api.VkApi(token=vk_token)
api = vk_session.get_api()

def get_all_dialog_photos(dialog_id):
    photos = []
    offset = 0
    total_count = 200  # Максимальное количество сообщений за один запрос

    while True:
        try:
            # Получаем список сообщений с увеличивающимся offset
            messages = api.messages.getHistory(peer_id=dialog_id, count=total_count, offset=offset)

            # Если количество сообщений меньше total_count, значит мы получили все фотографии
            if len(messages['items']) < total_count:
                break

            # Проходим по сообщениям и добавляем фотографии в список
            for message in messages['items']:
                if 'attachments' in message:
                    for attachment in message['attachments']:
                        if attachment['type'] == 'photo':
                            sizes = attachment['photo']['sizes']
                            largest_photo = max(sizes, key=lambda s: s['width'] * s['height'])
                            photos.append(largest_photo['url'])

            # Увеличиваем offset для следующего запроса
            offset += total_count

            # Добавляем небольшую задержку между запросами
            time.sleep(1)  # Это помогает избежать блокировки API

        except VkApiError as e:
            print(f"Ошибка при получении данных о диалоге: {e}")
            return []

    return photos

def save_photo_urls_to_file(photos, filename='photo_urls.txt'):
    with open(filename, 'w', encoding='utf-8') as file:
        for url in photos:
            file.write(url + '\n')
    print(f"Файл '{filename}' успешно создан.")

def main():
    dialog_id = int(input("Введите ID диалога: "))
    photo_urls = get_all_dialog_photos(dialog_id)
    if photo_urls:
        save_photo_urls_to_file(photo_urls)
    else:
        print("Нет фотографий для сохранения.")

if __name__ == "__main__":
    main()

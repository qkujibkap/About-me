import datetime
import requests
import json
print('Введи слово:')
word = input()
print('Введи токен:')
token = input()
group = 'SPD-132'
params = {
    'json': 'true',
}
#CAAT

def get_image(word, params):
    url_cat = 'https://cataas.com/cat/says/' + word
    resp = requests.get(url_cat, params = params)
    url_image = resp.json()['url']
    image = requests.get(url_image)
    with open(word+".jpg", "wb") as file:
      file.write(image.content)
    return image.content

image = get_image(word, params)

#Yandex
def upload_yadisk(image, token, word):
    headers = {
        'Authorization': f'OAuth {token}'
    }
    params = {
        'path': 'SPD-132'}
    requests.put('https://cloud-api.yandex.net/v1/disk/resources', headers = headers, params = params)
    url_yadisk = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
    file_name = f'SPD-132/{word + datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".png"}'
    params = {
        'path': file_name}
    upload = requests.get(url_yadisk,
                          params = params,
                          headers = headers)
    if upload.status_code != 200:
        result = (f'Ошибка!\n'
                  f'{upload.status_code}\n'
                  f'{upload.text}')
    else:
        upload_link = upload.json()['href']
        upload_file = requests.put(upload_link, files = {'file':image})
        if upload_file.status_code != 201:
            result = (f'Ошибка!\n '
                      f'{upload_file.status_code}\n'
                      f'{upload.text}')
        else:
            info = requests.get(
                "https://cloud-api.yandex.net/v1/disk/resources",
                headers=headers,
                params={"path": file_name}
            )

            if info.status_code == 200:
                file_info = info.json()

                data = {
                    "name": file_info.get("name"),
                    "size": file_info.get("size"),
                    "mime_type": file_info.get("mime_type"),
                    "created": file_info.get("created")
                }

                with open("result.json", "w", encoding="utf-8") as f:
                    json.dump(data, f, ensure_ascii=False, indent=4)

                result = (f'Файл загружен на Я.Диск\n'
                          f'Информация о файле сохранена в result.json')
            else:
                result = (f'Ошибка при запросе информации:\n'
                          f' {info.status_code}\n'
                          f' {info.text}')
    return result

print (upload_yadisk(image, token, word))
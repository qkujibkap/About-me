import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Ключевые слова
KEYWORDS = ['дизайн', 'фото', 'web', 'python']

# URL страницы со статьями
BASE_URL = "https://habr.com"
URL = "https://habr.com/ru/articles/"

# Настройка запроса
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/116.0.0.0 Safari/537.36"
}

# Загружаем страницу
response = requests.get(URL, headers=headers)
response.raise_for_status()

# Парсим HTML
soup = BeautifulSoup(response.text, "html.parser")

# Ищем статьи
articles = soup.find_all("article")

print(f"Найдено статей: {len(articles)}\n")

# Функция для проверки ключевых слов
def contains_keyword(text: str, keywords) -> bool:
    text = text.lower()
    return any(kw.lower() in text for kw in keywords)

# Обрабатываем статьи
for art in articles:
    # Заголовок
    title_tag = art.find("h2")
    if not title_tag:
        continue

    title = title_tag.get_text(strip=True)

    # Ссылка
    a_tag = title_tag.find("a")
    link = urljoin(BASE_URL, a_tag["href"]) if a_tag else None

    # Дата
    date_tag = art.find("time")
    date = date_tag.get_text(strip=True) if date_tag else "неизвестно"

    # Текст превью (весь текст блока статьи)
    preview = art.get_text(separator=" ", strip=True)

    # Проверяем ключевые слова
    if contains_keyword(preview, KEYWORDS):
        print(f"{date} – {title} – {link}")
# Структура Бота

## Файл favorites.json
Файл для сохранения избранных
 
    1. vk_id
    id пользователя для индетификации записи

    2. first_name, last_name
    Имя и фамилия для того что бы знать как зовут

    3. profile_url
    Ссылка на страницу для удобного перехода на страницу пользователя

    4. photos
    Фото пользователя для визуализации пользователя
    
    5. saved_at
    Дата сохранения для истории

## Файл config.py:
Для безопасности в репозитории лежит без токенов.

Настройки бота 
    
    TOKEN_GROUP - Токен группы

    GROUP_ID - ID Группы
    
    TOKEN_USER - Токен пользователя
    
    SEARCH_PARAMS - Параметры поиска
    
    FAVORITES_FILE - Файл для избранных

## Файл favorites.py:
Работа с файлом избранные

## Файл vk_client.py:
Файл клиента ВК

## Файл bot.py:
Основной код бота

# Контакты:

<a href="https://t.me/pkujibkaq">
  <img src="https://img.shields.io/badge/Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white" alt="Telegram">
</a>
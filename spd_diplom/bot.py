# bot.py
import os
import random
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api import VkApi
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_client import VKClient
from favorites import add_to_favorites, get_favorites
from config import TOKEN_GROUP, TOKEN_USER, GROUP_ID
vk_session = VkApi(token=TOKEN_GROUP)
longpoll = VkBotLongPoll(vk_session, GROUP_ID)
vk = vk_session.get_api()

client = VKClient(TOKEN_USER)  # поиск делаем от имени пользователя


def make_keyboard():
    kb = VkKeyboard(one_time=False)
    kb.add_button("Следующий", color=VkKeyboardColor.PRIMARY)
    kb.add_button("Добавить в избранное", color=VkKeyboardColor.POSITIVE)
    kb.add_line()
    kb.add_button("Показать избранных", color=VkKeyboardColor.PRIMARY)
    return kb.get_keyboard()


def send_user_card(peer_id: int, user_item: dict):
    owner_id = user_item["id"]
    name = f"{user_item.get('first_name')} {user_item.get('last_name')}"
    profile_url = f"https://vk.com/{user_item.get('domain') or owner_id}"
    attachments = client.get_top_photos(owner_id)
    text = f"{name}\n{profile_url}"
    vk.messages.send(peer_id=peer_id, random_id=random.randint(1, 1_000_000_000),
                     message=text, attachment=",".join(attachments) if attachments else None,
                     keyboard=make_keyboard())


def handle_show_favorites(peer_id: int):
    favs = get_favorites()
    if not favs:
        vk.messages.send(peer_id=peer_id, random_id=random.randint(1, 1_000_000_000),
                         message="Список избранных пуст.", keyboard=make_keyboard())
        return
    # Отправляем построчно первые 5 для примера
    for u in favs[:10]:
        txt = f"{u.get('first_name')} {u.get('last_name')} — {u.get('profile_url')}\nДобавлен: {u.get('_added_at')}"
        attachments = u.get("photos", [])
        vk.messages.send(peer_id=peer_id, random_id=random.randint(1, 1_000_000_000),
                         message=txt, attachment=",".join(attachments) if attachments else None)
    # напоминание
    vk.messages.send(peer_id=peer_id, random_id=random.randint(1, 1_000_000_000),
                     message="Это первые записи. Для полного списка открой favorites.json в проекте.",
                     keyboard=make_keyboard())


def run_bot():
    """
    Простая логика:
     - при получении любого сообщения — запускаем поиск и показываем первого кандидата (demo).
     - кнопки "Следующий", "Добавить в избранное", "Показать избранных".
    """
    print("Bot started...")
    # Для demo — будем хранить state в памяти (peer_id -> offset)
    user_state = {}

    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            payload = event.message.payload  # может быть None
            text = event.message.text
            peer_id = event.message.peer_id

            # инициализация
            state = user_state.get(peer_id, {"offset": 0, "last_shown": None})
            offset = state["offset"]

            if text.lower() == "показать избранных":
                handle_show_favorites(peer_id)
                continue

            if text.lower() in ("следующий", "next"):
                offset += 1
                user_state[peer_id] = {"offset": offset, "last_shown": None}
                # fallthrough — покажем следующего ниже

            if text.lower() in ("добавить в избранное", "favorite", "fav"):
                last = state.get("last_shown")
                if not last:
                    vk.messages.send(peer_id=peer_id, random_id=random.randint(1, 1_000_000_000),
                                     message="Нет последнего показанного пользователя, чтобы добавить.")
                    continue
                # подготовим структуру для сохранения
                user_info = client.get_user_info(str(last["id"]))
                attachments = client.get_top_photos(last["id"], count_top=3)
                to_save = {
                    "id": user_info["id"],
                    "first_name": user_info["first_name"],
                    "last_name": user_info["last_name"],
                    "profile_url": user_info["profile_url"],
                    "photos": attachments
                }
                added = add_to_favorites(to_save)
                vk.messages.send(peer_id=peer_id, random_id=random.randint(1, 1_000_000_000),
                                 message="Добавлено в избранное." if added else "Уже в избранных.")
                continue

            # По умолчанию — простой поиск: для demo используем жесткие параметры (например, возраст 25-35, любой пол)
            results = client.search_users(age_from=25, age_to=35, count=50, offset=offset * 50)
            if not results:
                vk.messages.send(peer_id=peer_id, random_id=random.randint(1, 1_000_000_000),
                                 message="Кандидатов не найдено. Попробуйте изменить критерии.")
                continue

            candidate = results[0]
            # Сохраняем последнее показанное
            user_state[peer_id] = {"offset": offset, "last_shown": candidate}
            send_user_card(peer_id, candidate)


if __name__ == "__main__":
    run_bot()
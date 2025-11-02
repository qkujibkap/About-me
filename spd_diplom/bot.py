import random
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from config import TOKEN_GROUP, TOKEN_USER, GROUP_ID
from vk_client import VKClient

# --- Сессии ---
vk_session = vk_api.VkApi(token=TOKEN_GROUP)
vk = vk_session.get_api()
longpoll = VkBotLongPoll(vk_session, GROUP_ID, wait=5)
user_session = vk_api.VkApi(token=TOKEN_USER)
user_vk = user_session.get_api()
client = VKClient(user_vk)

running = True
shown_users = set()           # чтобы не показывать повторно
last_shown_user = {}          # последний показанный пользователь для каждого peer_id

# --- клавиатура ---
def make_keyboard():
    kb = VkKeyboard(one_time=False)
    kb.add_button("Следующий", color=VkKeyboardColor.POSITIVE)
    kb.add_button("В избранное", color=VkKeyboardColor.NEGATIVE)
    kb.add_line()
    kb.add_button("Показать избранных", color=VkKeyboardColor.SECONDARY)
    kb.add_line()
    kb.add_button("Стоп", color=VkKeyboardColor.NEGATIVE)
    return kb.get_keyboard()

# --- отправка карточки пользователя ---
def send_user_card(peer_id, user):
    message = f"{user['first_name']} {user['last_name']}\nhttps://vk.com/id{user['id']}"
    attachments = []
    photos = client.get_top_photos(user['id'])
    for photo in photos:
        attachments.append(f"photo{photo['owner_id']}_{photo['id']}")
    vk.messages.send(
        user_id=peer_id,
        random_id=0,
        message=message,
        attachment=",".join(attachments),
        keyboard=make_keyboard()
    )

# --- основной цикл ---
def run_bot():
    global running
    print("Bot started...")
    try:
        while running:
            for event in longpoll.listen():
                if event.type == VkBotEventType.MESSAGE_NEW and event.from_user:
                    peer_id = event.message.peer_id
                    text = event.message.text.strip().lower()

                    if text == "начать":
                        vk.messages.send(
                            user_id=peer_id,
                            random_id=0,
                            message="Привет! Я помогу найти интересных людей 😉",
                            keyboard=make_keyboard()
                        )

                    elif text == "следующий":
                        while True:
                            offset = random.randint(0, 1000)
                            results = client.search_users(offset=offset)
                            if results and results[0]['id'] not in shown_users:
                                candidate = results[0]
                                shown_users.add(candidate['id'])
                                last_shown_user[peer_id] = candidate  # сохраняем для избранного
                                send_user_card(peer_id, candidate)
                                break

                    elif text == "в избранное":
                        if peer_id in last_shown_user:
                            user = last_shown_user[peer_id]
                            favorites = client.get_favorites()
                            # проверка, есть ли пользователь в избранных
                            if any(fav['id'] == user['id'] for fav in favorites):
                                vk.messages.send(
                                    user_id=peer_id,
                                    random_id=0,
                                    message=f"{user['first_name']} уже в избранном ⭐",
                                    keyboard=make_keyboard()
                                )
                            else:
                                client.add_to_favorites(user)
                                vk.messages.send(
                                    user_id=peer_id,
                                    random_id=0,
                                    message=f"{user['first_name']} добавлен(а) в избранное ⭐",
                                    keyboard=make_keyboard()
                                )
                        else:
                            vk.messages.send(
                                user_id=peer_id,
                                random_id=0,
                                message="Сначала нажмите «Следующий», чтобы выбрать пользователя.",
                                keyboard=make_keyboard()
                            )

                    elif text == "показать избранных":
                        favorites = client.get_favorites()
                        if not favorites:
                            msg = "Список избранных пуст 🙃"
                        else:
                            msg = "⭐ Избранные:\n" + "\n".join(
                                [f"{u['first_name']} {u['last_name']} — https://vk.com/id{u['id']}" for u in favorites]
                            )
                        vk.messages.send(
                            user_id=peer_id,
                            random_id=0,
                            message=msg,
                            keyboard=make_keyboard()
                        )

                    elif text == "стоп":
                        vk.messages.send(
                            user_id=peer_id,
                            random_id=0,
                            message="Бот остановлен ✅",
                            keyboard=make_keyboard()
                        )
                        print("Bot stopped by user command")
                        running = False
                        break

                    else:
                        vk.messages.send(
                            user_id=peer_id,
                            random_id=0,
                            message="Не понял команду 😅\nДоступные команды:\n- Начать\n- Следующий\n- В избранное\n- Показать избранных\n- Стоп",
                            keyboard=make_keyboard()
                        )

    except KeyboardInterrupt:
        print("Bot stopped manually")

if __name__ == "__main__":
    run_bot()
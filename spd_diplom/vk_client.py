import json
from typing import List, Dict, Any
from config import SEARCH_PARAMS, FAVORITES_FILE

class VKClient:
    def __init__(self, vk):
        self.vk = vk

    # --- Поиск пользователей с offset ---
    def search_users(self, offset: int = 0) -> List[Dict[str, Any]]:
        params = SEARCH_PARAMS.copy()
        params.update({
            "offset": offset,
            "has_photo": 1,
            "fields": "photo_id,city,domain,bdate",
            "status": 1
        })
        try:
            resp = self.vk.users.search(**params)
            return resp.get("items", [])
        except Exception as e:
            print(f"Ошибка при поиске пользователей: {e}")
            return []

    # --- Получаем топ-3 фото пользователя ---
    def get_top_photos(self, user_id: int, album: str = "profile") -> list:
        try:
            resp = self.vk.photos.get(owner_id=user_id, album_id=album, extended=1)
            items = resp.get("items", [])
            items.sort(key=lambda x: x.get("likes", {}).get("count", 0), reverse=True)
            return items[:3]
        except Exception as e:
            print(f"Ошибка при получении фото пользователя {user_id}: {e}")
            return []

    # --- Работа с избранными ---
    def load_favorites(self) -> List[Dict[str, Any]]:
        try:
            with open(FAVORITES_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            return []

    def save_favorites(self, data: List[Dict[str, Any]]):
        with open(FAVORITES_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def add_to_favorites(self, user: Dict[str, Any]):
        data = self.load_favorites()
        if user not in data:
            data.append(user)
            self.save_favorites(data)

    def get_favorites(self) -> List[Dict[str, Any]]:
        return self.load_favorites()
# vk_client.py
from typing import Dict, Any, List, Optional
import vk_api

# Пример: token может быть group token или user token с правами friends, photos
class VKClient:
    def __init__(self, token: str, api_version: str = "5.131"):
        self.vk = vk_api.VkApi(token=token).get_api()
        self.api_version = api_version

    def get_user_info(self, user_id: str) -> Dict[str, Any]:
        """Возвращает базовую информацию о пользователе."""
        resp = self.vk.users.get(user_ids=user_id, fields="city,sex,photo_max,domain")
        if not resp:
            raise ValueError("user not found")
        u = resp[0]
        return {
            "id": u["id"],
            "first_name": u.get("first_name"),
            "last_name": u.get("last_name"),
            "city": u.get("city", {}).get("title") if isinstance(u.get("city"), dict) else None,
            "sex": u.get("sex"),
            "photo": u.get("photo_max"),
            "profile_url": f"https://vk.com/{u.get('domain') or u['id']}"
        }

    def search_users(self, age_from: Optional[int] = None, age_to: Optional[int] = None,
                     sex: Optional[int] = None, city_id: Optional[int] = None,
                     offset: int = 0, count: int = 100) -> List[Dict[str, Any]]:
        """
        Выполняет users.search. count не более 1000 в целом, за один вызов можно до 1000.
        sex: 1 — female, 2 — male, 0 — any
        """
        params = {
            "count": count,
            "offset": offset,
            "fields": "city,domain,sex,photo_max",
        }
        if age_from: params["age_from"] = age_from
        if age_to: params["age_to"] = age_to
        if sex in (1, 2): params["sex"] = sex
        if city_id: params["city"] = city_id

        resp = self.vk.users.search(**params)
        return resp.get("items", [])

    def get_top_photos(self, owner_id: int, count_top: int = 3) -> List[str]:
        """
        Берёт фото профиля (album_id='profile') и возвращает список attachment-строк
        вида "photo{owner_id}_{photo_id}" для отправки в messages.send
        Берём photos.get (extended=1 чтобы получить likes).
        """
        try:
            photos_resp = self.vk.photos.get(owner_id=owner_id, album_id="profile", extended=1, count=200)
            items = photos_resp.get("items", [])
        except vk_api.exceptions.ApiError:
            return []

        # сортировка по лайкам (descending)
        items_sorted = sorted(items, key=lambda it: it.get("likes", {}).get("count", 0), reverse=True)
        top = items_sorted[:count_top]
        attachments = []
        for it in top:
            pid = it["id"]
            attachments.append(f"photo{owner_id}_{pid}")
        return attachments
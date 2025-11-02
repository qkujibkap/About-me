# favorites.py
import json
import os
from datetime import datetime
from typing import List, Dict, Any

FAVORITES_FILE = "favorites.json"


def _ensure_file_exists():
    if not os.path.exists(FAVORITES_FILE):
        with open(FAVORITES_FILE, "w", encoding="utf-8") as f:
            json.dump([], f, ensure_ascii=False, indent=2)


def load_favorites() -> List[Dict[str, Any]]:
    """Читает favorites.json. Если файл отсутствует — создаёт и возвращает []"""
    _ensure_file_exists()
    with open(FAVORITES_FILE, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
            if not isinstance(data, list):
                # если файл повреждён или не тот формат — пересоздаём
                data = []
            return data
        except json.JSONDecodeError:
            return []


def save_favorites(data: List[Dict[str, Any]]) -> None:
    """Записывает список в favorites.json"""
    with open(FAVORITES_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def get_favorites() -> List[Dict[str, Any]]:
    """Возвращает список избранных"""
    return load_favorites()


def add_to_favorites(user_data: Dict[str, Any]) -> bool:
    """
    Добавляет пользователя в избранные.
    user_data обязано содержать хотя бы 'id', 'first_name', 'last_name', 'profile_url', 'photos' (list).
    Возвращает True если добавлен, False если уже был.
    """
    if "id" not in user_data:
        raise ValueError("user_data must contain 'id' field")

    favorites = load_favorites()
    if any(u.get("id") == user_data["id"] for u in favorites):
        return False

    entry = user_data.copy()
    entry["_added_at"] = datetime.utcnow().isoformat() + "Z"
    favorites.append(entry)
    save_favorites(favorites)
    return True
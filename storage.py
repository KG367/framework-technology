"""Загрузка и сохранение данных проекта в JSON-файлах.

Модуль отвечает за преобразование между форматом JSON и объектами
моделей предметной области (Ingredient, Dish, Meal, UserProfile).
"""

import json
from pathlib import Path
from typing import Any, List

from models import Dish, Meal, UserProfile

DATA_DIR: Path = Path(__file__).parent / "data"
DISHES_FILE: Path = DATA_DIR / "dishes.json"
PLAN_FILE: Path = DATA_DIR / "plan.json"
USER_FILE: Path = DATA_DIR / "user.json"


def _read_json(path: Path, default: Any) -> Any:
    """Читает JSON-файл, возвращая default при ошибке."""
    if not path.exists():
        return default
    try:
        with open(path, "r", encoding="utf-8") as file:
            return json.load(file)
    except (json.JSONDecodeError, OSError):
        return default


def _write_json(path: Path, data: Any) -> None:
    """Сохраняет данные в JSON, создавая каталог при необходимости."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)


def load_dishes(path: Path = DISHES_FILE) -> List[Dish]:
    """Загружает каталог блюд из JSON, создавая объекты Dish."""
    raw = _read_json(path, [])
    if not isinstance(raw, list):
        return []
    dishes: List[Dish] = []
    for item in raw:
        if isinstance(item, dict):
            dishes.append(Dish.from_data(item))
    return dishes


def save_dishes(dishes: List[Dish], path: Path = DISHES_FILE) -> None:
    """Сохраняет объекты Dish в JSON."""
    _write_json(path, [dish.to_data() for dish in dishes])


def load_plan(
    dishes: List[Dish],
    path: Path = PLAN_FILE,
) -> List[Meal]:
    """Загружает план питания из JSON, связывая приёмы пищи с блюдами."""
    raw = _read_json(path, [])
    if not isinstance(raw, list):
        return []
    plan: List[Meal] = []
    for item in raw:
        if not isinstance(item, dict):
            continue
        meal = Meal.from_data(item, dishes)
        if meal is not None:
            plan.append(meal)
    return plan


def save_plan(plan: List[Meal], path: Path = PLAN_FILE) -> None:
    """Сохраняет объекты Meal в JSON."""
    _write_json(path, [meal.to_data() for meal in plan])


def load_user(path: Path = USER_FILE) -> UserProfile:
    """Загружает профиль пользователя из JSON."""
    raw = _read_json(path, None)
    if not isinstance(raw, dict):
        return UserProfile()
    return UserProfile.from_data(raw)


def save_user(user: UserProfile, path: Path = USER_FILE) -> None:
    """Сохраняет профиль пользователя в JSON."""
    _write_json(path, user.to_data())

"""Профиль пользователя: цели, бюджет и ограничения питания."""

from pathlib import Path
from typing import Any, Dict, List, Mapping, Optional, TypedDict, cast

from storage import read_json, write_json

DATA_FILE = Path(__file__).parent / "data" / "user.json"

KCAL_MIN = 500
KCAL_MAX = 10000

class UserProfile(TypedDict):
    """Профиль пользователя приложения."""

    name: str
    target_kcal: int
    budget: int
    restrictions: List[str]

def default_profile() -> UserProfile:
    """Возвращает профиль по умолчанию."""
    return {
        "name": "Пользователь",
        "target_kcal": 2000,
        "budget": 5000,
        "restrictions": [],
    }

def _read_int(source: Mapping[str, Any], key: str) -> Optional[int]:
    """Извлекает целое число из сырого словаря.

    Возвращает None, если значение отсутствует или не является целым
    числом. Значение bool отбрасывается — это не число в смысле JSON.
    """
    value = source.get(key)
    if isinstance(value, bool):
        return None
    if isinstance(value, int):
        return value
    return None

def _read_restrictions(source: Mapping[str, Any]) -> List[str]:
    """Извлекает список ограничений питания из сырого словаря."""
    value = source.get("restrictions")
    if not isinstance(value, list):
        return []
    result: List[str] = []
    for item in value:
        text = str(item).strip().lower()
        if text:
            result.append(text)
    return result

def load_user(path: Path = DATA_FILE) -> UserProfile:
    """Загружает профиль пользователя из JSON.

    Если файл отсутствует или повреждён, отсутствующие поля
    заполняются значениями по умолчанию.
    """
    raw = read_json(path, None)
    profile = default_profile()
    if not isinstance(raw, dict):
        return profile
    source: Dict[str, Any] = cast(Dict[str, Any], raw)

    name = source.get("name")
    if isinstance(name, str) and name.strip():
        profile["name"] = name.strip()

    kcal = _read_int(source, "target_kcal")
    if kcal is not None and KCAL_MIN <= kcal <= KCAL_MAX:
        profile["target_kcal"] = kcal

    budget = _read_int(source, "budget")
    if budget is not None and budget >= 0:
        profile["budget"] = budget

    profile["restrictions"] = _read_restrictions(source)
    return profile

def save_user(user: UserProfile, path: Path = DATA_FILE) -> None:
    """Сохраняет профиль пользователя в JSON."""
    write_json(path, dict(user))

def set_name(user: UserProfile, name: str) -> None:
    """Устанавливает имя пользователя.

    Возбуждает ValueError при пустой строке.
    """
    clean = name.strip()
    if not clean:
        raise ValueError("Имя не может быть пустым")
    user["name"] = clean

def set_target_kcal(user: UserProfile, target: int) -> None:
    """Устанавливает целевую калорийность дня.

    Возбуждает ValueError, если значение вне допустимого диапазона.
    """
    if not KCAL_MIN <= target <= KCAL_MAX:
        raise ValueError(
            "Целевая калорийность должна быть в диапазоне "
            f"{KCAL_MIN}–{KCAL_MAX}"
        )
    user["target_kcal"] = target

def set_budget(user: UserProfile, budget: int) -> None:
    """Устанавливает недельный бюджет.

    Возбуждает ValueError при отрицательном значении.
    """
    if budget < 0:
        raise ValueError("Бюджет не может быть отрицательным")
    user["budget"] = budget

def add_restriction(user: UserProfile, ingredient: str) -> bool:
    """Добавляет ограничение питания.

    Возвращает False, если ограничение уже есть.
    Возбуждает ValueError при пустом значении.
    """
    clean = ingredient.strip().lower()
    if not clean:
        raise ValueError("Название ингредиента не может быть пустым")
    if clean in user["restrictions"]:
        return False
    user["restrictions"].append(clean)
    return True

def remove_restriction(user: UserProfile, ingredient: str) -> bool:
    """Удаляет ограничение питания.

    Возвращает False, если такого ограничения не было.
    """
    clean = ingredient.strip().lower()
    if clean not in user["restrictions"]:
        return False
    user["restrictions"].remove(clean)
    return True

def is_dish_allowed(
    dish: Dict[str, Any],
    restrictions: List[str],
) -> bool:
    """Проверяет, что блюдо не содержит запрещённых ингредиентов."""
    if not restrictions:
        return True
    banned = {name.lower() for name in restrictions}
    for item in dish.get("ingredients", []):
        ingredient = str(item.get("name", "")).strip().lower()
        if ingredient in banned:
            return False
    return True

def filter_by_restrictions(
    dishes: List[Dict[str, Any]],
    restrictions: List[str],
) -> List[Dict[str, Any]]:
    """Отбирает блюда, не нарушающие ограничения питания."""
    if not restrictions:
        return list(dishes)
    return [
        dish for dish in dishes
        if is_dish_allowed(dish, restrictions)
    ]

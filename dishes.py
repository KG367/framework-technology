from pathlib import Path
from typing import Any, Dict, List, Optional

from storage import read_json

DATA_FILE = Path(__file__).parent / "data" / "dishes.json"


def load_dishes(path: Path = DATA_FILE) -> List[Dict[str, Any]]:
    """Загружает каталог блюд из JSON.

    Если файл повреждён или содержит не список — возвращает пустой список.
    """
    data = read_json(path, [])
    if not isinstance(data, list):
        return []
    return data


def find_by_name(
    dishes: List[Dict[str, Any]],
    name: str,
) -> Optional[Dict[str, Any]]:
    """Ищет блюдо по точному названию (без учёта регистра).

    Пустой запрос или запрос из пробелов возвращает None.
    """
    if not name:
        return None
    query = name.strip().lower()
    if not query:
        return None
    for dish in dishes:
        if query in dish.get("name", "").lower():
            return dish
    return None


def filter_dishes(
    dishes: List[Dict[str, Any]],
    slot: Optional[str] = None,
    max_minutes: Optional[int] = None,
) -> List[Dict[str, Any]]:
    """Фильтрует блюда по приёму пищи и максимальному времени готовки."""
    result: List[Dict[str, Any]] = []
    for dish in dishes:
        if slot is not None and dish.get("slot") != slot:
            continue
        if max_minutes is not None and dish.get("minutes", 0) > max_minutes:
            continue
        result.append(dish)
    return result

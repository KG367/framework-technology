"""Планирование приёмов пищи и построение списка покупок."""

from pathlib import Path
from typing import Any, Dict, List

from storage import read_json, write_json

DATA_FILE = Path(__file__).parent / "data" / "plan.json"
MEAL_SLOTS = ("завтрак", "обед", "ужин", "перекус")


def load_plan(path: Path = DATA_FILE) -> List[Dict[str, Any]]:
    """Загружает план питания из JSON."""
    data = read_json(path, [])
    if not isinstance(data, list):
        return []
    return data


def save_plan(plan: List[Dict[str, Any]], path: Path = DATA_FILE) -> None:
    """Сохраняет план питания в JSON."""
    write_json(path, plan)


def add_meal(
    plan: List[Dict[str, Any]],
    date: str,
    slot: str,
    dish_name: str,
    portions: int = 1,
) -> bool:
    """Добавляет приём пищи в план.

    Возвращает False, если слот на эту дату уже занят.
    Возбуждает ValueError при некорректных аргументах.
    """
    if slot not in MEAL_SLOTS:
        raise ValueError(f"Неизвестный приём пищи: {slot}")
    if portions < 1:
        raise ValueError("Число порций должно быть >= 1")
    for meal in plan:
        if meal["date"] == date and meal["slot"] == slot:
            return False
    plan.append({
        "date": date,
        "slot": slot,
        "dish": dish_name,
        "portions": portions,
    })
    return True


def remove_meal(
    plan: List[Dict[str, Any]],
    date: str,
    slot: str,
) -> bool:
    """Удаляет приём пищи; возвращает True, если запись найдена."""
    for index, meal in enumerate(plan):
        if meal["date"] == date and meal["slot"] == slot:
            del plan[index]
            return True
    return False


def total_calories(
    plan: List[Dict[str, Any]],
    dishes: List[Dict[str, Any]],
) -> int:
    """Считает суммарную калорийность всех блюд плана."""
    lookup = {dish["name"]: dish.get("kcal", 0) for dish in dishes}
    total = 0
    for meal in plan:
        portions = meal.get("portions", 1)
        total += lookup.get(meal["dish"], 0) * portions
    return total


def build_shopping_list(
    plan: List[Dict[str, Any]],
    dishes: List[Dict[str, Any]],
) -> Dict[str, List[str]]:
    """Собирает ингредиенты всех блюд плана.

    Возвращает словарь: имя ингредиента -> список количеств.
    """
    lookup = {dish["name"]: dish for dish in dishes}
    shopping: Dict[str, List[str]] = {}
    for meal in plan:
        dish = lookup.get(meal["dish"])
        if dish is None:
            continue
        for item in dish.get("ingredients", []):
            name = item.get("name", "").strip().lower()
            amount = item.get("amount", "")
            if not name:
                continue
            shopping.setdefault(name, []).append(amount)
    return shopping

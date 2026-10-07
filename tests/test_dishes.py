"""Тесты модуля dishes (pytest)."""

from typing import Optional, Union

import pytest

from dishes import filter_dishes, find_by_name

# --- Типы (подход А: простые словари через Union) ---

# Блюдо: {"name": "Омлет", "slot": "завтрак", "minutes": 10, "kcal": 320}
Dish = dict[str, Union[str, int]]

# Список блюд
DishList = list[Dish]

DISHES: DishList = [
    {"name": "Омлет", "slot": "завтрак", "minutes": 10, "kcal": 320},
    {"name": "Суп", "slot": "обед", "minutes": 60, "kcal": 350},
    {"name": "Салат", "slot": "ужин", "minutes": 15, "kcal": 200},
]

def test_find_by_name_ignoring_case() -> None:
    """Поиск не зависит от регистра."""
    dish: Optional[Dish] = find_by_name(DISHES, "омлет")
    assert dish is not None
    assert dish["name"] == "Омлет"

def test_find_by_name_not_found() -> None:
    """Неизвестное название возвращает None."""
    assert find_by_name(DISHES, "пицца") is None

def test_find_by_name_empty_query() -> None:
    """Пустой запрос возвращает None."""
    assert find_by_name(DISHES, "") is None

def test_filter_by_slot() -> None:
    """Фильтр по приёму пищи оставляет только совпадения."""
    result: DishList = filter_dishes(DISHES, slot="обед")
    assert len(result) == 1
    assert result[0]["name"] == "Суп"

def test_filter_by_minutes() -> None:
    """Фильтр по времени отбрасывает долгие блюда."""
    result: DishList = filter_dishes(DISHES, max_minutes=15)
    assert len(result) == 2

def test_filter_combined_no_match() -> None:
    """Комбинация фильтров может дать пустой результат."""
    result: DishList = filter_dishes(DISHES, slot="завтрак", max_minutes=5)
    assert result == []

def test_filter_without_conditions() -> None:
    """Без условий возвращаются все блюда."""
    result: DishList = filter_dishes(DISHES)
    assert len(result) == len(DISHES)

@pytest.mark.parametrize(
    "slot, max_minutes, expected",
    [
        ("завтрак", None, 1),
        (None, 15, 2),
        ("ужин", 20, 1),
        ("обед", 10, 0),
    ],
)
def test_filter_parametrized(
    slot: Optional[str], max_minutes: Optional[int], expected: int
) -> None:
    """Параметризованная проверка фильтра."""
    result: DishList = filter_dishes(DISHES, slot=slot, max_minutes=max_minutes)
    assert len(result) == expected
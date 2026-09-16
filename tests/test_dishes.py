"""Тесты модуля dishes (pytest)."""

import pytest

from dishes import filter_dishes, find_by_name

DISHES = [
    {"name": "Омлет", "slot": "завтрак", "minutes": 10, "kcal": 320},
    {"name": "Суп", "slot": "обед", "minutes": 60, "kcal": 350},
    {"name": "Салат", "slot": "ужин", "minutes": 15, "kcal": 200},
]


def test_find_by_name_ignoring_case():
    """Поиск не зависит от регистра."""
    dish = find_by_name(DISHES, "омлет")
    assert dish is not None
    assert dish["name"] == "Омлет"


def test_find_by_name_not_found():
    """Неизвестное название возвращает None."""
    assert find_by_name(DISHES, "пицца") is None


def test_find_by_name_empty_query():
    """Пустой запрос возвращает None."""
    assert find_by_name(DISHES, "") is None


def test_filter_by_slot():
    """Фильтр по приёму пищи оставляет только совпадения."""
    result = filter_dishes(DISHES, slot="обед")
    assert len(result) == 1
    assert result[0]["name"] == "Суп"


def test_filter_by_minutes():
    """Фильтр по времени отбрасывает долгие блюда."""
    result = filter_dishes(DISHES, max_minutes=15)
    assert len(result) == 2


def test_filter_combined_no_match():
    """Комбинация фильтров может дать пустой результат."""
    result = filter_dishes(DISHES, slot="завтрак", max_minutes=5)
    assert result == []


def test_filter_without_conditions():
    """Без условий возвращаются все блюда."""
    result = filter_dishes(DISHES)
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
def test_filter_parametrized(slot, max_minutes, expected):
    """Параметризованная проверка фильтра."""
    result = filter_dishes(DISHES, slot=slot, max_minutes=max_minutes)
    assert len(result) == expected

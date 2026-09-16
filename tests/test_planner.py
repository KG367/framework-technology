"""Тесты модуля planner (pytest)."""

import pytest

from planner import (
    add_meal,
    build_shopping_list,
    remove_meal,
    total_calories,
)

DISHES = [
    {
        "name": "Омлет",
        "kcal": 320,
        "ingredients": [
            {"name": "яйца", "amount": "3 шт"},
            {"name": "сыр", "amount": "50 г"},
        ],
    },
    {
        "name": "Салат",
        "kcal": 200,
        "ingredients": [{"name": "яйца", "amount": "2 шт"}],
    },
]


@pytest.fixture
def empty_plan():
    """Пустой план питания для каждого теста."""
    return []


@pytest.fixture
def one_meal_plan():
    """План с одним приёмом пищи."""
    return [
        {
            "date": "2026-09-17",
            "slot": "завтрак",
            "dish": "Омлет",
            "portions": 1,
        },
    ]


def test_add_meal_success(empty_plan):
    """Успешное добавление приёма пищи."""
    assert add_meal(empty_plan, "2026-09-17", "завтрак", "Омлет")
    assert len(empty_plan) == 1


def test_add_meal_conflict(empty_plan):
    """Повторная запись в тот же слот не добавляется."""
    add_meal(empty_plan, "2026-09-17", "завтрак", "Омлет")
    assert not add_meal(empty_plan, "2026-09-17", "завтрак", "Салат")
    assert len(empty_plan) == 1


def test_add_meal_unknown_slot(empty_plan):
    """Неизвестный слот вызывает ValueError."""
    with pytest.raises(ValueError):
        add_meal(empty_plan, "2026-09-17", "полдник", "Омлет")


@pytest.mark.parametrize("portions", [0, -1, -5])
def test_add_meal_bad_portions(empty_plan, portions):
    """Неположительное число порций вызывает ValueError."""
    with pytest.raises(ValueError):
        add_meal(empty_plan, "2026-09-17", "завтрак", "Омлет", portions)


def test_remove_existing_meal(one_meal_plan):
    """Удаление существующей записи возвращает True."""
    assert remove_meal(one_meal_plan, "2026-09-17", "завтрак")
    assert one_meal_plan == []


def test_remove_missing_meal(empty_plan):
    """Удаление несуществующей записи возвращает False."""
    assert not remove_meal(empty_plan, "2026-09-17", "завтрак")


def test_total_calories_single(one_meal_plan):
    """Одна порция одного блюда."""
    assert total_calories(one_meal_plan, DISHES) == 320


def test_total_calories_two_portions(one_meal_plan):
    """Калорийность умножается на число порций."""
    one_meal_plan[0]["portions"] = 2
    assert total_calories(one_meal_plan, DISHES) == 640


def test_total_calories_empty(empty_plan):
    """Пустой план даёт 0 ккал."""
    assert total_calories(empty_plan, DISHES) == 0


def test_shopping_list_merges_ingredients():
    """Ингредиенты из разных блюд объединяются."""
    plan = [
        {
            "date": "2026-09-17",
            "slot": "завтрак",
            "dish": "Омлет",
            "portions": 1,
        },
        {
            "date": "2026-09-17",
            "slot": "обед",
            "dish": "Салат",
            "portions": 1,
        },
    ]
    shopping = build_shopping_list(plan, DISHES)
    assert shopping["яйца"] == ["3 шт", "2 шт"]


def test_shopping_list_empty(empty_plan):
    """Пустой план даёт пустой список покупок."""
    assert build_shopping_list(empty_plan, DISHES) == {}


def test_shopping_list_ignores_unknown_dish():
    """Неизвестное блюдо в плане не ломает сборку."""
    plan = [
        {
            "date": "2026-09-17",
            "slot": "завтрак",
            "dish": "Пицца",
            "portions": 1,
        },
    ]
    assert build_shopping_list(plan, DISHES) == {}

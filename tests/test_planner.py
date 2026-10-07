"""Тесты модуля planner (pytest)."""

from typing import Union

import pytest

from planner import (
    add_meal,
    build_shopping_list,
    remove_meal,
    total_calories,
)

# --- Типы (подход А: простые словари через Union) ---

# Ингредиент: {"name": "яйца", "amount": "3 шт"}
Ingredient = dict[str, str]

# Блюдо: name/kcal + список ингредиентов
Dish = dict[str, Union[str, int, list[Ingredient]]]

# Запись плана: {"date": ..., "slot": ..., "dish": ..., "portions": ...}
Meal = dict[str, Union[str, int]]

# План питания — список приёмов пищи
Plan = list[Meal]

# Список покупок: ингредиент -> список количеств из разных блюд
ShoppingList = dict[str, list[str]]

DISHES: list[Dish] = [
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
def empty_plan() -> Plan:
    """Пустой план питания для каждого теста."""
    return []

@pytest.fixture
def one_meal_plan() -> Plan:
    """План с одним приёмом пищи."""
    return [
        {
            "date": "2026-09-17",
            "slot": "завтрак",
            "dish": "Омлет",
            "portions": 1,
        },
    ]

def test_add_meal_success(empty_plan: Plan) -> None:
    """Успешное добавление приёма пищи."""
    assert add_meal(empty_plan, "2026-09-17", "завтрак", "Омлет")
    assert len(empty_plan) == 1

def test_add_meal_conflict(empty_plan: Plan) -> None:
    """Повторная запись в тот же слот не добавляется."""
    add_meal(empty_plan, "2026-09-17", "завтрак", "Омлет")
    assert not add_meal(empty_plan, "2026-09-17", "завтрак", "Салат")
    assert len(empty_plan) == 1

def test_add_meal_unknown_slot(empty_plan: Plan) -> None:
    """Неизвестный слот вызывает ValueError."""
    with pytest.raises(ValueError):
        add_meal(empty_plan, "2026-09-17", "полдник", "Омлет")

@pytest.mark.parametrize("portions", [0, -1, -5])
def test_add_meal_bad_portions(empty_plan: Plan, portions: int) -> None:
    """Неположительное число порций вызывает ValueError."""
    with pytest.raises(ValueError):
        add_meal(empty_plan, "2026-09-17", "завтрак", "Омлет", portions)

def test_remove_existing_meal(one_meal_plan: Plan) -> None:
    """Удаление существующей записи возвращает True."""
    assert remove_meal(one_meal_plan, "2026-09-17", "завтрак")
    assert one_meal_plan == []

def test_remove_missing_meal(empty_plan: Plan) -> None:
    """Удаление несуществующей записи возвращает False."""
    assert not remove_meal(empty_plan, "2026-09-17", "завтрак")

def test_total_calories_single(one_meal_plan: Plan) -> None:
    """Одна порция одного блюда."""
    assert total_calories(one_meal_plan, DISHES) == 320

def test_total_calories_two_portions(one_meal_plan: Plan) -> None:
    """Калорийность умножается на число порций."""
    one_meal_plan[0]["portions"] = 2
    assert total_calories(one_meal_plan, DISHES) == 640

def test_total_calories_empty(empty_plan: Plan) -> None:
    """Пустой план даёт 0 ккал."""
    assert total_calories(empty_plan, DISHES) == 0

def test_shopping_list_merges_ingredients() -> None:
    """Ингредиенты из разных блюд объединяются."""
    plan: Plan = [
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
    shopping: ShoppingList = build_shopping_list(plan, DISHES)
    assert shopping["яйца"] == ["3 шт", "2 шт"]

def test_shopping_list_empty(empty_plan: Plan) -> None:
    """Пустой план даёт пустой список покупок."""
    assert build_shopping_list(empty_plan, DISHES) == {}

def test_shopping_list_ignores_unknown_dish() -> None:
    """Неизвестное блюдо в плане не ломает сборку."""
    plan: Plan = [
        {
            "date": "2026-09-17",
            "slot": "завтрак",
            "dish": "Пицца",
            "portions": 1,
        },
    ]
    assert build_shopping_list(plan, DISHES) == {}

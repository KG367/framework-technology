"""Тесты модели Meal и функций плана питания."""

from typing import List

import pytest

from models import (
    Dish,
    Ingredient,
    Meal,
    UserProfile,
    add_meal,
    build_shopping_list,
    remove_meal,
    total_calories,
)


@pytest.fixture
def user() -> UserProfile:
    """Профиль тестового пользователя."""
    return UserProfile(name="Тестовый пользователь")


@pytest.fixture
def omelette() -> Dish:
    """Тестовое блюдо «Омлет»."""
    return Dish(
        "Омлет",
        "завтрак",
        10,
        320,
        [Ingredient("яйца", "3 шт"), Ingredient("сыр", "50 г")],
    )


@pytest.fixture
def salad() -> Dish:
    """Тестовое блюдо «Салат»."""
    return Dish(
        "Салат",
        "ужин",
        15,
        200,
        [Ingredient("яйца", "2 шт")],
    )


@pytest.fixture
def empty_plan() -> List[Meal]:
    """Пустой план питания."""
    return []


@pytest.fixture
def one_meal_plan(omelette: Dish, user: UserProfile) -> List[Meal]:
    """План с одним приёмом пищи."""
    return [Meal("2026-09-17", "завтрак", omelette, user, 1)]


def test_meal_creation(omelette: Dish, user: UserProfile) -> None:
    """Создание приёма пищи со ссылками на блюдо и пользователя."""
    meal = Meal("2026-09-17", "завтрак", omelette, user, 2)
    assert meal.date == "2026-09-17"
    assert meal.slot == "завтрак"
    assert meal.dish is omelette
    assert meal.user is user
    assert meal.portions == 2


def test_meal_str(omelette: Dish, user: UserProfile) -> None:
    """Строковое представление приёма пищи."""
    meal = Meal("2026-09-17", "завтрак", omelette, user, 2)
    text = str(meal)
    assert "Омлет" in text
    assert "x2" in text
    assert user.name in text


def test_meal_to_data(omelette: Dish, user: UserProfile) -> None:
    """Сериализация приёма пищи в словарь."""
    meal = Meal("2026-09-17", "завтрак", omelette, user, 1)
    data = meal.to_data()
    assert data == {
        "date": "2026-09-17",
        "slot": "завтрак",
        "dish": "Омлет",
        "user": user.name,
        "portions": 1,
    }


def test_meal_from_data(omelette: Dish, user: UserProfile) -> None:
    """Восстановление приёма пищи из словаря."""
    data = {
        "date": "2026-09-17",
        "slot": "завтрак",
        "dish": "Омлет",
        "user": user.name,
        "portions": 1,
    }
    meal = Meal.from_data(data, [omelette], user)
    assert meal is not None
    assert meal.dish is omelette
    assert meal.user is user


def test_meal_from_data_unknown_dish(
    omelette: Dish,
    user: UserProfile,
) -> None:
    """Неизвестное блюдо не создаёт приём пищи."""
    data = {
        "date": "2026-09-17",
        "slot": "завтрак",
        "dish": "Пицца",
        "user": user.name,
        "portions": 1,
    }
    assert Meal.from_data(data, [omelette], user) is None


def test_add_meal_success(
    empty_plan: List[Meal],
    omelette: Dish,
    user: UserProfile,
) -> None:
    """Успешное добавление приёма пищи."""
    assert add_meal(
        empty_plan, "2026-09-17", "завтрак", omelette, user
    )
    assert len(empty_plan) == 1
    assert empty_plan[0].user is user


def test_add_meal_conflict(
    empty_plan: List[Meal],
    omelette: Dish,
    salad: Dish,
    user: UserProfile,
) -> None:
    """Повторная запись в тот же слот не добавляется."""
    add_meal(empty_plan, "2026-09-17", "завтрак", omelette, user)
    assert not add_meal(
        empty_plan, "2026-09-17", "завтрак", salad, user
    )
    assert len(empty_plan) == 1


def test_add_meal_unknown_slot(
    empty_plan: List[Meal],
    omelette: Dish,
    user: UserProfile,
) -> None:
    """Неизвестный слот вызывает ValueError."""
    with pytest.raises(ValueError):
        add_meal(empty_plan, "2026-09-17", "полдник", omelette, user)


@pytest.mark.parametrize("portions", [0, -1, -5])
def test_add_meal_bad_portions(
    empty_plan: List[Meal],
    omelette: Dish,
    user: UserProfile,
    portions: int,
) -> None:
    """Неположительное число порций вызывает ValueError."""
    with pytest.raises(ValueError):
        add_meal(
            empty_plan,
            "2026-09-17",
            "завтрак",
            omelette,
            user,
            portions,
        )


def test_remove_existing_meal(one_meal_plan: List[Meal]) -> None:
    """Удаление существующей записи возвращает True."""
    assert remove_meal(one_meal_plan, "2026-09-17", "завтрак")
    assert one_meal_plan == []


def test_remove_missing_meal(empty_plan: List[Meal]) -> None:
    """Удаление несуществующей записи возвращает False."""
    assert not remove_meal(empty_plan, "2026-09-17", "завтрак")


def test_total_calories_single(one_meal_plan: List[Meal]) -> None:
    """Одна порция одного блюда."""
    assert total_calories(one_meal_plan) == 320


def test_total_calories_two_portions(one_meal_plan: List[Meal]) -> None:
    """Калорийность умножается на число порций."""
    one_meal_plan[0].portions = 2
    assert total_calories(one_meal_plan) == 640


def test_total_calories_empty(empty_plan: List[Meal]) -> None:
    """Пустой план даёт 0 ккал."""
    assert total_calories(empty_plan) == 0


def test_shopping_list_merges_ingredients(
    omelette: Dish,
    salad: Dish,
    user: UserProfile,
) -> None:
    """Ингредиенты из разных блюд объединяются."""
    plan = [
        Meal("2026-09-17", "завтрак", omelette, user, 1),
        Meal("2026-09-17", "обед", salad, user, 1),
    ]
    shopping = build_shopping_list(plan)
    assert shopping["яйца"] == ["3 шт", "2 шт"]


def test_shopping_list_empty(empty_plan: List[Meal]) -> None:
    """Пустой план даёт пустой список покупок."""
    assert build_shopping_list(empty_plan) == {}

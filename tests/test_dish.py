"""Тесты модели Dish и функций каталога блюд."""

from typing import List, Optional

import pytest

from models import (
    Dish,
    Ingredient,
    filter_dishes,
    find_by_name,
    find_dish_by_id,
)


def make_dish(
    dish_id: int,
    name: str,
    slot: str,
    minutes: int,
    kcal: int,
) -> Dish:
    """Создаёт тестовое блюдо без ингредиентов."""
    return Dish(
        dish_id=dish_id,
        name=name,
        slot=slot,
        minutes=minutes,
        kcal=kcal,
        ingredients=[],
    )


@pytest.fixture
def dishes() -> List[Dish]:
    """Каталог тестовых блюд."""
    return [
        make_dish(1, "Омлет", "завтрак", 10, 320),
        make_dish(2, "Суп", "обед", 60, 350),
        make_dish(3, "Салат", "ужин", 15, 200),
    ]


def test_dish_creation() -> None:
    """Создание блюда с ингредиентами."""
    ingredient = Ingredient("яйца", "3 шт")
    dish = Dish(1, "Омлет", "завтрак", 10, 320, [ingredient])
    assert dish.dish_id == 1
    assert dish.name == "Омлет"
    assert dish.slot == "завтрак"
    assert dish.minutes == 10
    assert dish.kcal == 320
    assert len(dish.ingredients) == 1


def test_dish_str() -> None:
    """Строковое представление блюда."""
    dish = make_dish(1, "Омлет", "завтрак", 10, 320)
    assert str(dish) == "Омлет | завтрак | 10 мин | 320 ккал"


def test_ingredient_str() -> None:
    """Строковое представление ингредиента."""
    ingredient = Ingredient("яйца", "3 шт")
    assert str(ingredient) == "яйца: 3 шт"


def test_dish_is_allowed_without_restrictions() -> None:
    """Без ограничений любое блюдо разрешено."""
    dish = Dish(
        1, "Омлет", "завтрак", 10, 320,
        [Ingredient("яйца", "3 шт")],
    )
    assert dish.is_allowed([])


def test_dish_is_allowed_blocked() -> None:
    """Блюдо с запрещённым ингредиентом не пропускается."""
    dish = Dish(
        1,
        "Паста",
        "обед",
        20,
        520,
        [Ingredient("паста", "200 г"), Ingredient("орехи", "50 г")],
    )
    assert not dish.is_allowed(["орехи"])


def test_dish_from_data_roundtrip() -> None:
    """Создание блюда из словаря и обратное преобразование."""
    data = {
        "id": 1,
        "name": "Омлет",
        "slot": "завтрак",
        "minutes": 10,
        "kcal": 320,
        "ingredients": [{"name": "яйца", "amount": "3 шт"}],
    }
    dish = Dish.from_data(data)
    assert dish.dish_id == 1
    assert dish.name == "Омлет"
    assert dish.ingredients[0].name == "яйца"
    assert dish.to_data() == data


def test_find_by_name_ignoring_case(dishes: List[Dish]) -> None:
    """Поиск не зависит от регистра."""
    dish: Optional[Dish] = find_by_name(dishes, "омлет")
    assert dish is not None
    assert dish.name == "Омлет"


def test_find_by_name_not_found(dishes: List[Dish]) -> None:
    """Неизвестное название возвращает None."""
    assert find_by_name(dishes, "пицца") is None


def test_find_by_name_empty_query(dishes: List[Dish]) -> None:
    """Пустой запрос возвращает None."""
    assert find_by_name(dishes, "") is None


def test_find_dish_by_id_found(dishes: List[Dish]) -> None:
    """Поиск блюда по существующему id."""
    dish = find_dish_by_id(dishes, 2)
    assert dish is not None
    assert dish.name == "Суп"


def test_find_dish_by_id_not_found(dishes: List[Dish]) -> None:
    """Поиск блюда по отсутствующему id даёт None."""
    assert find_dish_by_id(dishes, 999) is None


def test_filter_by_slot(dishes: List[Dish]) -> None:
    """Фильтр по приёму пищи оставляет только совпадения."""
    result = filter_dishes(dishes, slot="обед")
    assert len(result) == 1
    assert result[0].name == "Суп"


def test_filter_by_minutes(dishes: List[Dish]) -> None:
    """Фильтр по времени отбрасывает долгие блюда."""
    result = filter_dishes(dishes, max_minutes=15)
    assert len(result) == 2


def test_filter_combined_no_match(dishes: List[Dish]) -> None:
    """Комбинация фильтров может дать пустой результат."""
    result = filter_dishes(dishes, slot="завтрак", max_minutes=5)
    assert result == []


def test_filter_without_conditions(dishes: List[Dish]) -> None:
    """Без условий возвращаются все блюда."""
    result = filter_dishes(dishes)
    assert len(result) == len(dishes)


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
    dishes: List[Dish],
    slot: Optional[str],
    max_minutes: Optional[int],
    expected: int,
) -> None:
    """Параметризованная проверка фильтра."""
    result = filter_dishes(dishes, slot=slot, max_minutes=max_minutes)
    assert len(result) == expected

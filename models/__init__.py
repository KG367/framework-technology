"""Пакет объектной модели предметной области.

Экспортирует классы Ingredient, Dish, UserProfile, Meal и функции
обработки коллекций этих объектов. Порядок импортов соответствует
графу зависимостей: ingredient -> dish -> user -> meal.
"""

from .dish import Dish, filter_dishes, find_by_name, find_dish_by_id
from .ingredient import Ingredient
from .meal import (
    MEAL_SLOTS,
    Meal,
    add_meal,
    build_shopping_list,
    find_meal,
    find_meal_by_id,
    remove_meal,
    total_calories,
)
from .user import KCAL_MAX, KCAL_MIN, UserProfile

__all__ = [
    "Dish",
    "Ingredient",
    "Meal",
    "UserProfile",
    "KCAL_MAX",
    "KCAL_MIN",
    "MEAL_SLOTS",
    "add_meal",
    "build_shopping_list",
    "filter_dishes",
    "find_by_name",
    "find_dish_by_id",
    "find_meal",
    "find_meal_by_id",
    "remove_meal",
    "total_calories",
]

"""Пакет объектной модели предметной области.

Экспортирует классы Ingredient, Dish, Meal, UserProfile и функции
обработки коллекций этих объектов.
"""

from .dish import Dish, filter_dishes, find_by_name
from .ingredient import Ingredient
from .meal import (
    MEAL_SLOTS,
    Meal,
    add_meal,
    build_shopping_list,
    find_meal,
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
    "find_meal",
    "remove_meal",
    "total_calories",
]

"""Блюдо и функции работы с каталогом блюд."""

from typing import Any, Dict, List, Optional

from .ingredient import Ingredient


class Dish:
    """Блюдо: идентификатор, название, приём пищи, состав."""

    def __init__(
        self,
        dish_id: int,
        name: str,
        slot: str,
        minutes: int,
        kcal: int,
        ingredients: List[Ingredient],
    ) -> None:
        """Создаёт блюдо с указанными характеристиками."""
        self.dish_id: int = dish_id
        self.name: str = name.strip()
        self.slot: str = slot.strip().lower()
        self.minutes: int = minutes
        self.kcal: int = kcal
        self.ingredients: List[Ingredient] = list(ingredients)

    def __str__(self) -> str:
        """Возвращает строковое представление блюда."""
        return (
            f"{self.name} | {self.slot} | "
            f"{self.minutes} мин | {self.kcal} ккал"
        )

    def is_allowed(self, restrictions: List[str]) -> bool:
        """Проверяет, что блюдо не содержит запрещённых ингредиентов."""
        if not restrictions:
            return True
        banned = {name.lower() for name in restrictions}
        for ingredient in self.ingredients:
            if ingredient.name.lower() in banned:
                return False
        return True

    @classmethod
    def from_data(cls, data: Dict[str, Any]) -> "Dish":
        """Создаёт блюдо из словаря (например, из JSON)."""
        dish_id = int(data.get("id", 0))
        name = str(data.get("name", "")).strip()
        slot = str(data.get("slot", "")).strip().lower()
        minutes = int(data.get("minutes", 0))
        kcal = int(data.get("kcal", 0))
        raw_ingredients = data.get("ingredients", [])
        ingredients: List[Ingredient] = []
        if isinstance(raw_ingredients, list):
            for item in raw_ingredients:
                if isinstance(item, dict):
                    ingredients.append(Ingredient.from_data(item))
        return cls(dish_id, name, slot, minutes, kcal, ingredients)

    def to_data(self) -> Dict[str, Any]:
        """Преобразует блюдо в словарь для сохранения в JSON."""
        return {
            "id": self.dish_id,
            "name": self.name,
            "slot": self.slot,
            "minutes": self.minutes,
            "kcal": self.kcal,
            "ingredients": [item.to_data() for item in self.ingredients],
        }


def find_by_name(dishes: List[Dish], name: str) -> Optional[Dish]:
    """Ищет блюдо по подстроке названия (без учёта регистра)."""
    if not name:
        return None
    query = name.strip().lower()
    if not query:
        return None
    for dish in dishes:
        if query in dish.name.lower():
            return dish
    return None


def find_dish_by_id(
    dishes: List[Dish],
    dish_id: int,
) -> Optional[Dish]:
    """Ищет блюдо по идентификатору."""
    for dish in dishes:
        if dish.dish_id == dish_id:
            return dish
    return None


def filter_dishes(
    dishes: List[Dish],
    slot: Optional[str] = None,
    max_minutes: Optional[int] = None,
) -> List[Dish]:
    """Фильтрует блюда по приёму пищи и максимальному времени готовки."""
    result: List[Dish] = []
    for dish in dishes:
        if slot is not None and dish.slot != slot:
            continue
        if max_minutes is not None and dish.minutes > max_minutes:
            continue
        result.append(dish)
    return result

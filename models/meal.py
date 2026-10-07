"""Приём пищи и функции работы с планом питания."""

from typing import Any, Dict, List, Optional, Tuple

from .dish import Dish

MEAL_SLOTS: Tuple[str, ...] = ("завтрак", "обед", "ужин", "перекус")


class Meal:
    """Приём пищи: дата, слот, блюдо, число порций."""

    def __init__(
        self,
        date: str,
        slot: str,
        dish: Dish,
        portions: int = 1,
    ) -> None:
        """Создаёт приём пищи, связывая его с блюдом-объектом."""
        self.date: str = date
        self.slot: str = slot
        self.dish: Dish = dish
        self.portions: int = portions

    def __str__(self) -> str:
        """Возвращает строковое представление приёма пищи."""
        return (
            f"{self.date} | {self.slot} | "
            f"{self.dish.name} x{self.portions}"
        )

    def to_data(self) -> Dict[str, Any]:
        """Преобразует приём пищи в словарь для JSON.

        Ссылка на блюдо сохраняется как название.
        """
        return {
            "date": self.date,
            "slot": self.slot,
            "dish": self.dish.name,
            "portions": self.portions,
        }

    @classmethod
    def from_data(
        cls,
        data: Dict[str, Any],
        dishes: List[Dish],
    ) -> Optional["Meal"]:
        """Создаёт приём пищи из JSON, находя связанное блюдо в каталоге.

        Возвращает None, если блюдо с указанным названием не найдено.
        """
        name = str(data.get("dish", "")).strip()
        dish: Optional[Dish] = None
        for candidate in dishes:
            if candidate.name == name:
                dish = candidate
                break
        if dish is None:
            return None
        date = str(data.get("date", "")).strip()
        slot = str(data.get("slot", "")).strip().lower()
        portions = int(data.get("portions", 1))
        return cls(date, slot, dish, portions)


def find_meal(
    plan: List[Meal],
    date: str,
    slot: str,
) -> Optional[Meal]:
    """Находит приём пищи по дате и слоту."""
    for meal in plan:
        if meal.date == date and meal.slot == slot:
            return meal
    return None


def add_meal(
    plan: List[Meal],
    date: str,
    slot: str,
    dish: Dish,
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
    if find_meal(plan, date, slot) is not None:
        return False
    plan.append(Meal(date=date, slot=slot, dish=dish, portions=portions))
    return True


def remove_meal(
    plan: List[Meal],
    date: str,
    slot: str,
) -> bool:
    """Удаляет приём пищи; возвращает True, если запись найдена."""
    for index, meal in enumerate(plan):
        if meal.date == date and meal.slot == slot:
            del plan[index]
            return True
    return False


def total_calories(plan: List[Meal]) -> int:
    """Считает суммарную калорийность всех блюд плана."""
    total = 0
    for meal in plan:
        total += meal.dish.kcal * meal.portions
    return total


def build_shopping_list(plan: List[Meal]) -> Dict[str, List[str]]:
    """Собирает ингредиенты всех блюд плана.

    Возвращает словарь: имя ингредиента -> список количеств.
    """
    shopping: Dict[str, List[str]] = {}
    for meal in plan:
        for ingredient in meal.dish.ingredients:
            name = ingredient.name.lower()
            if not name:
                continue
            shopping.setdefault(name, []).append(ingredient.amount)
    return shopping

"""Профиль пользователя: цели, бюджет и ограничения питания."""

from typing import Any, Dict, List, Optional

from .dish import Dish

KCAL_MIN: int = 500
KCAL_MAX: int = 10000


class UserProfile:
    """Профиль пользователя приложения."""

    def __init__(
        self,
        name: str = "Пользователь",
        target_kcal: int = 2000,
        budget: int = 5000,
        restrictions: Optional[List[str]] = None,
    ) -> None:
        """Создаёт профиль с указанными значениями."""
        self.name: str = name
        self.target_kcal: int = target_kcal
        self.budget: int = budget
        self.restrictions: List[str] = list(restrictions) if restrictions else []

    def __str__(self) -> str:
        """Возвращает строковое представление профиля."""
        return (
            f"{self.name} | цель: {self.target_kcal} ккал/день | "
            f"бюджет: {self.budget} руб/неделя"
        )

    def set_name(self, name: str) -> None:
        """Устанавливает имя пользователя.

        Возбуждает ValueError при пустой строке.
        """
        clean = name.strip()
        if not clean:
            raise ValueError("Имя не может быть пустым")
        self.name = clean

    def set_target_kcal(self, target: int) -> None:
        """Устанавливает целевую калорийность дня.

        Возбуждает ValueError, если значение вне диапазона.
        """
        if not KCAL_MIN <= target <= KCAL_MAX:
            raise ValueError(
                "Целевая калорийность должна быть в диапазоне " f"{KCAL_MIN}–{KCAL_MAX}"
            )
        self.target_kcal = target

    def set_budget(self, budget: int) -> None:
        """Устанавливает недельный бюджет.

        Возбуждает ValueError при отрицательном значении.
        """
        if budget < 0:
            raise ValueError("Бюджет не может быть отрицательным")
        self.budget = budget

    def add_restriction(self, ingredient: str) -> bool:
        """Добавляет ограничение питания.

        Возвращает False, если ограничение уже есть.
        Возбуждает ValueError при пустом значении.
        """
        clean = ingredient.strip().lower()
        if not clean:
            raise ValueError("Название ингредиента не может быть пустым")
        if clean in self.restrictions:
            return False
        self.restrictions.append(clean)
        return True

    def remove_restriction(self, ingredient: str) -> bool:
        """Удаляет ограничение питания.

        Возвращает False, если такого ограничения не было.
        """
        clean = ingredient.strip().lower()
        if clean not in self.restrictions:
            return False
        self.restrictions.remove(clean)
        return True

    def is_dish_allowed(self, dish: Dish) -> bool:
        """Проверяет, что блюдо не нарушает ограничения профиля."""
        return dish.is_allowed(self.restrictions)

    def filter_dishes(self, dishes: List[Dish]) -> List[Dish]:
        """Отбирает блюда, не нарушающие ограничения профиля."""
        if not self.restrictions:
            return list(dishes)
        return [dish for dish in dishes if self.is_dish_allowed(dish)]

    @classmethod
    def from_data(cls, data: Dict[str, Any]) -> "UserProfile":
        """Создаёт профиль из словаря, отбрасывая некорректные значения."""
        name = "Пользователь"
        target_kcal = 2000
        budget = 5000
        restrictions: List[str] = []

        raw_name = data.get("name")
        if isinstance(raw_name, str) and raw_name.strip():
            name = raw_name.strip()

        raw_kcal = data.get("target_kcal")
        if (
            isinstance(raw_kcal, int)
            and not isinstance(raw_kcal, bool)
            and KCAL_MIN <= raw_kcal <= KCAL_MAX
        ):
            target_kcal = raw_kcal

        raw_budget = data.get("budget")
        if (
            isinstance(raw_budget, int)
            and not isinstance(raw_budget, bool)
            and raw_budget >= 0
        ):
            budget = raw_budget

        raw_restrictions = data.get("restrictions")
        if isinstance(raw_restrictions, list):
            for item in raw_restrictions:
                text = str(item).strip().lower()
                if text:
                    restrictions.append(text)

        return cls(name, target_kcal, budget, restrictions)

    def to_data(self) -> Dict[str, Any]:
        """Преобразует профиль в словарь для сохранения в JSON."""
        return {
            "name": self.name,
            "target_kcal": self.target_kcal,
            "budget": self.budget,
            "restrictions": list(self.restrictions),
        }

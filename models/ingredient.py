"""Ингредиент блюда."""

from typing import Any, Dict


class Ingredient:
    """Ингредиент, входящий в состав блюда."""

    def __init__(self, name: str, amount: str) -> None:
        """Создаёт ингредиент с указанным названием и количеством."""
        self.name: str = name.strip()
        self.amount: str = amount.strip()

    def __str__(self) -> str:
        """Возвращает строковое представление ингредиента."""
        return f"{self.name}: {self.amount}"

    @classmethod
    def from_data(cls, data: Dict[str, Any]) -> "Ingredient":
        """Создаёт ингредиент из словаря (например, из JSON)."""
        name = str(data.get("name", "")).strip()
        amount = str(data.get("amount", "")).strip()
        return cls(name, amount)

    def to_data(self) -> Dict[str, str]:
        """Преобразует ингредиент в словарь для сохранения в JSON."""
        return {"name": self.name, "amount": self.amount}

"""Тесты модели UserProfile."""

from pathlib import Path

import pytest

from models import Dish, Ingredient, UserProfile
from storage import load_user, save_user


@pytest.fixture
def profile() -> UserProfile:
    """Свежий профиль по умолчанию."""
    return UserProfile()


def test_default_profile_has_expected_fields() -> None:
    """Профиль по умолчанию содержит все поля."""
    user = UserProfile()
    assert user.name == "Пользователь"
    assert user.target_kcal == 2000
    assert user.budget == 5000
    assert user.restrictions == []


def test_set_name_strips_whitespace(profile: UserProfile) -> None:
    """Имя устанавливается без лишних пробелов."""
    profile.set_name("  Анна  ")
    assert profile.name == "Анна"


def test_set_name_empty_raises(profile: UserProfile) -> None:
    """Пустое имя вызывает ValueError."""
    with pytest.raises(ValueError):
        profile.set_name("   ")


def test_set_target_kcal_ok(profile: UserProfile) -> None:
    """Корректная калорийность сохраняется."""
    profile.set_target_kcal(1800)
    assert profile.target_kcal == 1800


@pytest.mark.parametrize("value", [0, 100, 499, 10001])
def test_set_target_kcal_out_of_range(
    profile: UserProfile,
    value: int,
) -> None:
    """Значение вне диапазона вызывает ValueError."""
    with pytest.raises(ValueError):
        profile.set_target_kcal(value)


def test_set_budget_ok(profile: UserProfile) -> None:
    """Корректный бюджет сохраняется."""
    profile.set_budget(7500)
    assert profile.budget == 7500


def test_set_budget_negative_raises(profile: UserProfile) -> None:
    """Отрицательный бюджет вызывает ValueError."""
    with pytest.raises(ValueError):
        profile.set_budget(-1)


def test_add_restriction_first_time(profile: UserProfile) -> None:
    """Первое добавление возвращает True."""
    assert profile.add_restriction("Орехи")
    assert "орехи" in profile.restrictions


def test_add_restriction_duplicate(profile: UserProfile) -> None:
    """Повторное добавление возвращает False."""
    profile.add_restriction("орехи")
    assert not profile.add_restriction("ОРЕХИ")
    assert profile.restrictions == ["орехи"]


def test_add_restriction_empty_raises(profile: UserProfile) -> None:
    """Пустое название вызывает ValueError."""
    with pytest.raises(ValueError):
        profile.add_restriction("  ")


def test_remove_restriction_existing(profile: UserProfile) -> None:
    """Удаление существующего ограничения возвращает True."""
    profile.add_restriction("орехи")
    assert profile.remove_restriction("Орехи")
    assert profile.restrictions == []


def test_remove_restriction_missing(profile: UserProfile) -> None:
    """Удаление несуществующего возвращает False."""
    assert not profile.remove_restriction("орехи")


def test_is_dish_allowed_without_restrictions(
    profile: UserProfile,
) -> None:
    """Без ограничений любое блюдо разрешено."""
    dish = Dish("Омлет", "завтрак", 10, 320, [Ingredient("яйца", "3 шт")])
    assert profile.is_dish_allowed(dish)


def test_is_dish_allowed_blocked(profile: UserProfile) -> None:
    """Блюдо с запрещённым ингредиентом не пропускается."""
    profile.add_restriction("орехи")
    dish = Dish("Паста", "обед", 20, 520, [Ingredient("орехи", "50 г")])
    assert not profile.is_dish_allowed(dish)


def test_filter_dishes_removes(profile: UserProfile) -> None:
    """Фильтр убирает блюда с запрещёнными ингредиентами."""
    profile.add_restriction("орехи")
    dishes = [
        Dish("Омлет", "завтрак", 10, 320, [Ingredient("яйца", "3 шт")]),
        Dish("Паста", "обед", 20, 520, [Ingredient("орехи", "50 г")]),
        Dish("Салат", "ужин", 15, 200, [Ingredient("салат", "100 г")]),
    ]
    allowed = profile.filter_dishes(dishes)
    names = [dish.name for dish in allowed]
    assert "Паста" not in names
    assert "Омлет" in names
    assert "Салат" in names


def test_filter_dishes_empty_returns_all(profile: UserProfile) -> None:
    """Без ограничений возвращаются все блюда."""
    dishes = [
        Dish("Омлет", "завтрак", 10, 320, []),
        Dish("Салат", "ужин", 15, 200, []),
    ]
    assert profile.filter_dishes(dishes) == dishes


def test_save_and_load_roundtrip(tmp_path: Path) -> None:
    """Профиль корректно сохраняется и загружается."""
    path = tmp_path / "user.json"
    original = UserProfile()
    original.set_name("Дмитрий")
    original.set_target_kcal(2600)
    original.add_restriction("орехи")
    save_user(original, path)

    restored = load_user(path)
    assert restored.name == "Дмитрий"
    assert restored.target_kcal == 2600
    assert restored.restrictions == ["орехи"]


def test_load_user_missing_file(tmp_path: Path) -> None:
    """Отсутствующий файл даёт профиль по умолчанию."""
    path = tmp_path / "nope.json"
    user = load_user(path)
    assert user.name == "Пользователь"


def test_load_user_broken_types(tmp_path: Path) -> None:
    """Повреждённые значения заменяются значениями по умолчанию."""
    path = tmp_path / "user.json"
    path.write_text(
        '{"name": 42, "target_kcal": "abc", '
        '"budget": -10, "restrictions": "нет"}',
        encoding="utf-8",
    )
    user = load_user(path)
    assert user.name == "Пользователь"
    assert user.target_kcal == 2000
    assert user.budget == 5000
    assert user.restrictions == []

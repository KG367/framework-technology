"""Тесты модуля user (pytest)."""

from pathlib import Path

import pytest

from user import (
    KCAL_MAX,
    KCAL_MIN,
    UserProfile,
    add_restriction,
    default_profile,
    filter_by_restrictions,
    is_dish_allowed,
    load_user,
    remove_restriction,
    save_user,
    set_budget,
    set_name,
    set_target_kcal,
)

DISHES = [
    {
        "name": "Омлет",
        "slot": "завтрак",
        "ingredients": [
            {"name": "яйца", "amount": "3 шт"},
            {"name": "сыр", "amount": "50 г"},
        ],
    },
    {
        "name": "Паста с орехами",
        "slot": "обед",
        "ingredients": [
            {"name": "паста", "amount": "200 г"},
            {"name": "орехи", "amount": "50 г"},
        ],
    },
    {
        "name": "Салат",
        "slot": "ужин",
        "ingredients": [
            {"name": "салат", "amount": "100 г"},
        ],
    },
]

@pytest.fixture
def profile() -> UserProfile:
    """Свежий профиль по умолчанию для каждого теста."""
    return default_profile()

def test_default_profile_has_expected_fields() -> None:
    """Профиль по умолчанию содержит все поля."""
    user = default_profile()
    assert user["name"] == "Пользователь"
    assert user["target_kcal"] == 2000
    assert user["budget"] == 5000
    assert user["restrictions"] == []

def test_set_name_strips_whitespace(profile: UserProfile) -> None:
    """Имя устанавливается без лишних пробелов."""
    set_name(profile, "  Анна  ")
    assert profile["name"] == "Анна"

def test_set_name_empty_raises(profile: UserProfile) -> None:
    """Пустое имя вызывает ValueError."""
    with pytest.raises(ValueError):
        set_name(profile, "   ")

def test_set_target_kcal_ok(profile: UserProfile) -> None:
    """Корректная калорийность сохраняется."""
    set_target_kcal(profile, 1800)
    assert profile["target_kcal"] == 1800

@pytest.mark.parametrize(
    "value",
    [0, 100, KCAL_MIN - 1, KCAL_MAX + 1],
)
def test_set_target_kcal_out_of_range(
    profile: UserProfile,
    value: int,
) -> None:
    """Значение вне диапазона вызывает ValueError."""
    with pytest.raises(ValueError):
        set_target_kcal(profile, value)

def test_set_budget_ok(profile: UserProfile) -> None:
    """Корректный бюджет сохраняется."""
    set_budget(profile, 7500)
    assert profile["budget"] == 7500

def test_set_budget_negative_raises(profile: UserProfile) -> None:
    """Отрицательный бюджет вызывает ValueError."""
    with pytest.raises(ValueError):
        set_budget(profile, -1)

def test_add_restriction_first_time(profile: UserProfile) -> None:
    """Первое добавление возвращает True."""
    assert add_restriction(profile, "Орехи")
    assert "орехи" in profile["restrictions"]

def test_add_restriction_duplicate(profile: UserProfile) -> None:
    """Повторное добавление возвращает False."""
    add_restriction(profile, "орехи")
    assert not add_restriction(profile, "ОРЕХИ")
    assert profile["restrictions"] == ["орехи"]

def test_add_restriction_empty_raises(profile: UserProfile) -> None:
    """Пустое название вызывает ValueError."""
    with pytest.raises(ValueError):
        add_restriction(profile, "  ")

def test_remove_restriction_existing(profile: UserProfile) -> None:
    """Удаление существующего ограничения возвращает True."""
    add_restriction(profile, "орехи")
    assert remove_restriction(profile, "Орехи")
    assert profile["restrictions"] == []

def test_remove_restriction_missing(profile: UserProfile) -> None:
    """Удаление несуществующего возвращает False."""
    assert not remove_restriction(profile, "орехи")

def test_is_dish_allowed_without_restrictions() -> None:
    """Без ограничений любое блюдо разрешено."""
    assert is_dish_allowed(DISHES[0], [])

def test_is_dish_allowed_blocked() -> None:
    """Блюдо с запрещённым ингредиентом не пропускается."""
    assert not is_dish_allowed(DISHES[1], ["орехи"])

def test_filter_by_restrictions_removes() -> None:
    """Фильтр убирает блюда с запрещёнными ингредиентами."""
    allowed = filter_by_restrictions(DISHES, ["орехи"])
    names = [dish["name"] for dish in allowed]
    assert "Паста с орехами" not in names
    assert "Омлет" in names
    assert "Салат" in names

def test_filter_by_restrictions_empty_returns_all() -> None:
    """Без ограничений возвращаются все блюда."""
    allowed = filter_by_restrictions(DISHES, [])
    assert len(allowed) == len(DISHES)

def test_save_and_load_roundtrip(tmp_path: Path) -> None:
    """Профиль корректно сохраняется и загружается."""
    path = tmp_path / "user.json"
    original = default_profile()
    original["name"] = "Дмитрий"
    original["target_kcal"] = 2600
    original["restrictions"] = ["орехи"]
    save_user(original, path)

    restored = load_user(path)
    assert restored["name"] == "Дмитрий"
    assert restored["target_kcal"] == 2600
    assert restored["restrictions"] == ["орехи"]

def test_load_user_missing_file(tmp_path: Path) -> None:
    """Отсутствующий файл даёт профиль по умолчанию."""
    path = tmp_path / "nope.json"
    user = load_user(path)
    assert user["name"] == "Пользователь"

def test_load_user_broken_types(tmp_path: Path) -> None:
    """Повреждённые значения заменяются на значения по умолчанию."""
    path = tmp_path / "user.json"
    path.write_text(
        '{"name": 42, "target_kcal": "abc", '
        '"budget": -10, "restrictions": "нет"}',
        encoding="utf-8",
    )
    user = load_user(path)
    assert user["name"] == "Пользователь"
    assert user["target_kcal"] == 2000
    assert user["budget"] == 5000
    assert user["restrictions"] == []

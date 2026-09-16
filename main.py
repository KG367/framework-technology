"""Точка входа: интерактивное меню системы планирования питания."""

from typing import Any, Dict, List

from dishes import filter_dishes, find_by_name, load_dishes
from planner import (
    add_meal,
    build_shopping_list,
    load_plan,
    remove_meal,
    save_plan,
    total_calories,
)
from utils import ask_int, format_date, parse_date


def show_dishes(dishes: List[Dict[str, Any]]) -> None:
    """Печатает каталог блюд."""
    print("\n--- Каталог блюд ---")
    for dish in dishes:
        print(
            f"  {dish['name']} | {dish['slot']} | "
            f"{dish['minutes']} мин | {dish['kcal']} ккал"
        )


def show_plan(plan: List[Dict[str, Any]]) -> None:
    """Печатает план питания, отсортированный по дате и слоту."""
    if not plan:
        print("\nПлан пуст.")
        return
    print("\n--- План питания ---")
    ordered = sorted(plan, key=lambda m: (m["date"], m["slot"]))
    for meal in ordered:
        print(
            f"  {format_date(meal['date'])} | {meal['slot']} | "
            f"{meal['dish']} x{meal['portions']}"
        )


def handle_find(dishes: List[Dict[str, Any]]) -> None:
    """Обрабатывает поиск блюда по названию."""
    name = input("Название блюда: ").strip()
    dish = find_by_name(dishes, name)
    if dish is None:
        print("Блюдо не найдено.")
        return
    print(
        f"Найдено: {dish['name']}, "
        f"{dish['minutes']} мин, {dish['kcal']} ккал"
    )
    for item in dish.get("ingredients", []):
        print(f"  - {item['name']}: {item['amount']}")


def handle_filter(dishes: List[Dict[str, Any]]) -> None:
    """Обрабатывает подбор блюд по слоту и времени."""
    slot = input("Приём пищи (завтрак/обед/ужин/перекус): ").strip().lower()
    minutes = ask_int("Максимум минут: ")
    if minutes is None:
        print("Нужно целое число.")
        return
    found = filter_dishes(dishes, slot=slot, max_minutes=minutes)
    if not found:
        print("Ничего не подошло.")
        return
    for dish in found:
        print(f"  {dish['name']} ({dish['minutes']} мин)")


def handle_add(
    dishes: List[Dict[str, Any]],
    plan: List[Dict[str, Any]],
) -> None:
    """Добавляет блюдо в план питания."""
    iso_date = parse_date(input("Дата (ДД.ММ.ГГГГ): "))
    if iso_date is None:
        print("Неверный формат даты.")
        return
    slot = input("Приём пищи: ").strip().lower()
    name = input("Название блюда: ").strip()
    if find_by_name(dishes, name) is None:
        print("Такого блюда нет в каталоге.")
        return
    portions = ask_int("Порций: ")
    if portions is None or portions < 1:
        print("Нужно целое число >= 1.")
        return
    try:
        added = add_meal(plan, iso_date, slot, name, portions)
    except ValueError as exc:
        print(f"Ошибка: {exc}")
        return
    if added:
        save_plan(plan)
        print("Добавлено в план.")
    else:
        print("Этот слот уже занят.")


def handle_remove(plan: List[Dict[str, Any]]) -> None:
    """Удаляет приём пищи из плана."""
    iso_date = parse_date(input("Дата (ДД.ММ.ГГГГ): "))
    if iso_date is None:
        print("Неверный формат даты.")
        return
    slot = input("Приём пищи: ").strip().lower()
    if remove_meal(plan, iso_date, slot):
        save_plan(plan)
        print("Удалено.")
    else:
        print("Ничего не найдено.")


def handle_shopping(
    dishes: List[Dict[str, Any]],
    plan: List[Dict[str, Any]],
) -> None:
    """Печатает список покупок."""
    shopping = build_shopping_list(plan, dishes)
    if not shopping:
        print("Список покупок пуст.")
        return
    print("\n--- Список покупок ---")
    for name in sorted(shopping):
        amounts = ", ".join(shopping[name])
        print(f"  {name}: {amounts}")


def handle_stats(
    dishes: List[Dict[str, Any]],
    plan: List[Dict[str, Any]],
) -> None:
    """Печатает статистику по плану."""
    print(f"\nБлюд в плане: {len(plan)}")
    print(f"Суммарная калорийность: {total_calories(plan, dishes)} ккал")


MENU = (
    ("1", "Показать каталог блюд"),
    ("2", "Найти блюдо по названию"),
    ("3", "Подобрать блюдо по времени"),
    ("4", "Добавить блюдо в план"),
    ("5", "Удалить блюдо из плана"),
    ("6", "Показать план"),
    ("7", "Список покупок"),
    ("8", "Статистика"),
    ("0", "Выход"),
)


def print_menu() -> None:
    """Печатает главное меню."""
    print("\n=== Система планирования питания ===")
    for key, title in MENU:
        print(f"{key}. {title}")


def main() -> None:
    """Главный цикл приложения."""
    dishes = load_dishes()
    if not dishes:
        print("Каталог блюд пуст. Проверьте data/dishes.json.")
        return

    plan = load_plan()

    actions = {
        "1": lambda: show_dishes(dishes),
        "2": lambda: handle_find(dishes),
        "3": lambda: handle_filter(dishes),
        "4": lambda: handle_add(dishes, plan),
        "5": lambda: handle_remove(plan),
        "6": lambda: show_plan(plan),
        "7": lambda: handle_shopping(dishes, plan),
        "8": lambda: handle_stats(dishes, plan),
    }

    while True:
        print_menu()
        choice = input("Выберите действие: ").strip()
        if choice == "0":
            print("До свидания!")
            return
        action = actions.get(choice)
        if action is None:
            print("Неизвестное действие.")
        else:
            action()


if __name__ == "__main__":
    main()

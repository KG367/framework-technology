"""Точка входа: интерактивное меню системы планирования питания.

Основные данные хранятся в виде коллекций объектов предметной области:
List[Dish], List[Meal] и UserProfile. main.py не содержит словарей
и не дублирует логику работы с моделями.
"""

from typing import Callable, Dict, List, Tuple

from models import (
    MEAL_SLOTS,
    Dish,
    Meal,
    UserProfile,
    add_meal,
    build_shopping_list,
    filter_dishes,
    find_by_name,
    remove_meal,
    total_calories,
)
from storage import (
    load_dishes,
    load_plan,
    load_user,
    save_plan,
    save_user,
)
from utils import ask_int, format_date, parse_date

MENU: Tuple[Tuple[str, str], ...] = (
    ("1", "Показать каталог блюд"),
    ("2", "Найти блюдо по названию"),
    ("3", "Подобрать блюдо по времени"),
    ("4", "Добавить блюдо в план"),
    ("5", "Удалить блюдо из плана"),
    ("6", "Показать план"),
    ("7", "Список покупок"),
    ("8", "Статистика"),
    ("9", "Показать профиль"),
    ("10", "Настроить профиль"),
    ("11", "Ограничения питания"),
    ("12", "Подобрать блюда без ограничений"),
    ("0", "Выход"),
)


def show_dishes(dishes: List[Dish]) -> None:
    """Печатает каталог блюд."""
    print("\n--- Каталог блюд ---")
    for dish in dishes:
        print(f"  {dish}")


def show_plan(plan: List[Meal]) -> None:
    """Печатает план питания, отсортированный по дате и слоту."""
    if not plan:
        print("\nПлан пуст.")
        return
    print("\n--- План питания ---")
    ordered = sorted(plan, key=lambda m: (m.date, m.slot))
    for meal in ordered:
        print(
            f"  {format_date(meal.date)} | {meal.slot} | "
            f"{meal.dish.name} x{meal.portions} "
            f"({meal.user.name})"
        )


def show_profile(user: UserProfile) -> None:
    """Печатает профиль пользователя."""
    print("\n--- Профиль ---")
    print(f"  Имя: {user.name}")
    print(f"  Цель по калориям: {user.target_kcal} ккал/день")
    print(f"  Бюджет: {user.budget} руб/неделя")
    if user.restrictions:
        print(f"  Ограничения: {', '.join(user.restrictions)}")
    else:
        print("  Ограничения: нет")


def handle_find(dishes: List[Dish]) -> None:
    """Обрабатывает поиск блюда по названию."""
    name = input("Название блюда: ").strip()
    dish = find_by_name(dishes, name)
    if dish is None:
        print("Блюдо не найдено.")
        return
    print(f"Найдено: {dish}")
    for ingredient in dish.ingredients:
        print(f"  - {ingredient}")


def handle_filter(dishes: List[Dish]) -> None:
    """Обрабатывает подбор блюд по слоту и времени."""
    slot = input(
        "Приём пищи (завтрак/обед/ужин/перекус): "
    ).strip().lower()
    minutes = ask_int("Максимум минут: ")
    if minutes is None:
        print("Нужно целое число.")
        return
    found = filter_dishes(dishes, slot=slot, max_minutes=minutes)
    if not found:
        print("Ничего не подошло.")
        return
    for dish in found:
        print(f"  {dish}")


def handle_add(
    dishes: List[Dish],
    plan: List[Meal],
    user: UserProfile,
) -> None:
    """Добавляет блюдо в план питания пользователя."""
    iso_date = parse_date(input("Дата (ДД.ММ.ГГГГ): "))
    if iso_date is None:
        print("Неверный формат даты.")
        return
    slot = input("Приём пищи: ").strip().lower()
    name = input("Название блюда: ").strip()
    dish = find_by_name(dishes, name)
    if dish is None:
        print("Такого блюда нет в каталоге.")
        return
    portions = ask_int("Порций: ")
    if portions is None or portions < 1:
        print("Нужно целое число >= 1.")
        return
    try:
        added = add_meal(plan, iso_date, slot, dish, user, portions)
    except ValueError as exc:
        print(f"Ошибка: {exc}")
        return
    if added:
        save_plan(plan)
        print("Добавлено в план.")
    else:
        print("Этот слот уже занят.")


def handle_remove(plan: List[Meal]) -> None:
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


def handle_shopping(plan: List[Meal]) -> None:
    """Печатает список покупок."""
    shopping = build_shopping_list(plan)
    if not shopping:
        print("Список покупок пуст.")
        return
    print("\n--- Список покупок ---")
    for name in sorted(shopping):
        amounts = ", ".join(shopping[name])
        print(f"  {name}: {amounts}")


def handle_stats(plan: List[Meal], user: UserProfile) -> None:
    """Печатает статистику по плану и сравнивает с целью."""
    total = total_calories(plan)
    print(f"\nБлюд в плане: {len(plan)}")
    print(f"Суммарная калорийность: {total} ккал")
    if user.target_kcal > 0 and plan:
        days = len({meal.date for meal in plan}) or 1
        average = total // days
        print(
            f"Цель: {user.target_kcal} ккал/день, "
            f"среднее: {average} ккал/день"
        )


def handle_set_name(user: UserProfile) -> None:
    """Изменяет имя пользователя."""
    name = input("Новое имя: ").strip()
    try:
        user.set_name(name)
    except ValueError as exc:
        print(f"Ошибка: {exc}")
        return
    save_user(user)
    print("Имя обновлено.")


def handle_set_kcal(user: UserProfile) -> None:
    """Изменяет целевую калорийность."""
    target = ask_int("Целевая калорийность (ккал/день): ")
    if target is None:
        print("Нужно целое число.")
        return
    try:
        user.set_target_kcal(target)
    except ValueError as exc:
        print(f"Ошибка: {exc}")
        return
    save_user(user)
    print("Цель обновлена.")


def handle_set_budget(user: UserProfile) -> None:
    """Изменяет недельный бюджет."""
    budget = ask_int("Бюджет на неделю (руб): ")
    if budget is None:
        print("Нужно целое число.")
        return
    try:
        user.set_budget(budget)
    except ValueError as exc:
        print(f"Ошибка: {exc}")
        return
    save_user(user)
    print("Бюджет обновлён.")


def handle_edit_profile(user: UserProfile) -> None:
    """Субменю редактирования профиля."""
    while True:
        print("\n--- Настройка профиля ---")
        print("1. Изменить имя")
        print("2. Изменить цель по калориям")
        print("3. Изменить бюджет")
        print("0. Назад")
        choice = input("Действие: ").strip()
        if choice == "0":
            return
        if choice == "1":
            handle_set_name(user)
        elif choice == "2":
            handle_set_kcal(user)
        elif choice == "3":
            handle_set_budget(user)
        else:
            print("Неизвестное действие.")


def handle_restrictions(user: UserProfile) -> None:
    """Субменю управления ограничениями питания."""
    while True:
        print("\n--- Ограничения питания ---")
        if user.restrictions:
            print("Текущие:", ", ".join(user.restrictions))
        else:
            print("Текущие: нет")
        print("1. Добавить")
        print("2. Удалить")
        print("0. Назад")
        choice = input("Действие: ").strip()
        if choice == "0":
            return
        if choice == "1":
            name = input("Ингредиент: ").strip()
            try:
                added = user.add_restriction(name)
            except ValueError as exc:
                print(f"Ошибка: {exc}")
                continue
            if added:
                save_user(user)
                print("Добавлено.")
            else:
                print("Такое ограничение уже есть.")
        elif choice == "2":
            name = input("Ингредиент: ").strip()
            if user.remove_restriction(name):
                save_user(user)
                print("Удалено.")
            else:
                print("Такого ограничения нет.")
        else:
            print("Неизвестное действие.")


def handle_safe_filter(dishes: List[Dish], user: UserProfile) -> None:
    """Подбор блюд с учётом ограничений питания."""
    allowed = user.filter_dishes(dishes)
    if not allowed:
        print("Нет блюд, удовлетворяющих ограничениям.")
        return
    print(f"\nДоступно блюд: {len(allowed)} из {len(dishes)}")
    for dish in allowed:
        print(f"  {dish}")


def setup_data() -> Tuple[List[Dish], List[Meal], UserProfile]:
    """Загружает каталог блюд, профиль и план пользователя.
    """
    user = load_user()
    dishes = load_dishes()
    plan = load_plan(dishes, user)
    return dishes, plan, user


def build_actions(
    dishes: List[Dish],
    plan: List[Meal],
    user: UserProfile,
) -> Dict[str, Callable[[], None]]:
    """Собирает таблицу обработчиков для пунктов меню."""
    return {
        "1": lambda: show_dishes(dishes),
        "2": lambda: handle_find(dishes),
        "3": lambda: handle_filter(dishes),
        "4": lambda: handle_add(dishes, plan, user),
        "5": lambda: handle_remove(plan),
        "6": lambda: show_plan(plan),
        "7": lambda: handle_shopping(plan),
        "8": lambda: handle_stats(plan, user),
        "9": lambda: show_profile(user),
        "10": lambda: handle_edit_profile(user),
        "11": lambda: handle_restrictions(user),
        "12": lambda: handle_safe_filter(dishes, user),
    }


def print_menu() -> None:
    """Печатает главное меню."""
    print("\n=== Система планирования питания ===")
    for key, title in MENU:
        print(f"{key}. {title}")


def run_loop(actions: Dict[str, Callable[[], None]]) -> None:
    """Главный цикл: показывает меню и вызывает выбранный обработчик."""
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


def main() -> None:
    """Точка входа приложения."""
    dishes, plan, user = setup_data()
    if not dishes:
        print("Каталог блюд пуст. Проверьте data/dishes.json.")
        return
    print(f"Доступные приёмы пищи: {', '.join(MEAL_SLOTS)}")
    actions = build_actions(dishes, plan, user)
    run_loop(actions)


if __name__ == "__main__":
    main()

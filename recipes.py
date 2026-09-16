# Модуль с данными о блюдах и простыми функциями поиска.
# Сценарий: "Что приготовить сейчас?" — подбор блюда по приёму пищи,
# доступному времени и наличию главного продукта.

# Каждое блюдо — словарь с простыми типами данных: str, int
DISHES = [
    {"name": "Омлет с сыром",     "slot": "завтрак", "minutes": 10, "main": "яйца",     "kcal": 320},
    {"name": "Овсяная каша",      "slot": "завтрак", "minutes": 15, "main": "овсянка",  "kcal": 280},
    {"name": "Тост с авокадо",    "slot": "завтрак", "minutes":  7, "main": "хлеб",     "kcal": 250},
    {"name": "Паста с томатами",  "slot": "обед",    "minutes": 20, "main": "паста",    "kcal": 520},
    {"name": "Куриный суп",       "slot": "обед",    "minutes": 60, "main": "курица",   "kcal": 350},
    {"name": "Гречка с котлетой", "slot": "ужин",    "minutes": 30, "main": "гречка",   "kcal": 480},
    {"name": "Салат с тунцом",    "slot": "ужин",    "minutes": 15, "main": "тунец",    "kcal": 260},
]

def all_slots():
    """Возвращает список допустимых приёмов пищи."""
    return ["завтрак", "обед", "ужин"]

def find_dishes(slot, minutes, product):
    """Подбирает блюда по трём условиям: приём пищи, время, главный продукт."""
    result = []
    for dish in DISHES:
        if dish["slot"] == slot and dish["minutes"] <= minutes and dish["main"] == product:
            result.append(dish)
    return result

def count_total_calories(dishes):
    """Суммирует калории найденных блюд (простое преобразование к int)."""
    total = 0
    for dish in dishes:
        total = total + int(dish["kcal"])
    return total

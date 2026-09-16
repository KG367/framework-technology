import recipes

print("=== Что приготовить? ===")

slot = input("Приём пищи (завтрак/обед/ужин): ").strip().lower()

if slot not in recipes.all_slots():
    print("Неизвестный приём пищи. Доступно:", ", ".join(recipes.all_slots()))
else:
    minutes_text = input("Сколько минут у тебя есть? ").strip()

    if not minutes_text.isdigit():
        print("Нужно ввести целое число минут.")
    else:
        minutes = int(minutes_text)
        product = input("Какой главный продукт есть? ").strip().lower()

        found = recipes.find_dishes(slot, minutes, product)

        if len(found) == 0:
            print("Ничего не подошло. Попробуй другое время или продукт.")
        else:
            print("\nНайдено вариантов:", len(found))
            for dish in found:
                print("  •", dish["name"], "—", dish["minutes"], "мин, ~", dish["kcal"], "ккал")

            total = recipes.count_total_calories(found)
            print("Суммарная калорийность вариантов:", total, "ккал")

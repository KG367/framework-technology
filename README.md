# Система планирования приготовления блюд

Консольное и веб приложение для планирования домашнего питания.

## Назначение

Приложение позволяет:

- просматривать каталог блюд с ингредиентами;
- искать блюда по названию;
- подбирать блюда по приёму пищи и времени готовки;
- планировать приёмы пищи на даты;
- удалять приёмы пищи из плана;
- строить список покупок из плана;
- подсчитывать калорийность;
- вести профиль пользователя (цель по калориям, бюджет);
- управлять ограничениями питания (аллергии, диеты);
- сохранять все данные в JSON-файлах.

## Предметная область

Домашнее питание: планирование меню, закупка ингредиентов и учёт
ограничений в питании.

## Модель предметной области

### Ingredient — ингредиент блюда

- `name` — название ингредиента;
- `amount` — количество (например, «3 шт», «50 г»).

Методы: `__str__`, `from_data`, `to_data`.

### Dish — блюдо

- `dish_id` — идентификатор (используется в URL `/dishes/<id>/`);
- `name` — название блюда;
- `slot` — приём пищи;
- `minutes` — время готовки;
- `kcal` — калорийность одной порции;
- `ingredients` — список объектов `Ingredient`.

Методы: `__str__`, `is_allowed(restrictions)`, `from_data`, `to_data`.

### UserProfile — профиль пользователя

- `name`, `target_kcal`, `budget`, `restrictions`.

Методы: `set_name`, `set_target_kcal`, `set_budget`,
`add_restriction`, `remove_restriction`, `is_dish_allowed`,
`filter_dishes`, `from_data`, `to_data`.

### Meal — приём пищи

Объект `Meal` связывает блюдо и пользователя.

- `meal_id` — идентификатор (используется в URL `/plan/<id>/`);
- `date` — ISO-дата (`YYYY-MM-DD`);
- `slot` — приём пищи;
- `dish: Dish` — ссылка на объект блюда;
- `user: UserProfile` — ссылка на объект пользователя;
- `portions` — число порций.

Методы: `__str__`, `from_data`, `to_data`.

## Функции обработки коллекций

| Функция | Модуль | Назначение |
|---|---|---|
| `find_by_name` | `models/dish.py` | поиск блюда по подстроке |
| `find_dish_by_id` | `models/dish.py` | поиск блюда по идентификатору |
| `filter_dishes` | `models/dish.py` | фильтр по слоту и времени |
| `find_meal` | `models/meal.py` | поиск приёма по дате и слоту |
| `find_meal_by_id` | `models/meal.py` | поиск приёма по идентификатору |
| `next_meal_id` | `models/meal.py` | следующий свободный id |
| `add_meal` / `remove_meal` | `models/meal.py` | добавление и удаление |
| `total_calories` | `models/meal.py` | суммарная калорийность |
| `build_shopping_list` | `models/meal.py` | агрегация ингредиентов |

## Веб-интерфейс (Django)

### Страницы

| URL | View | Назначение |
|---|---|---|
| `/` | `homepage.views.index` | главная, навигация |
| `/profile/` | `homepage.views.profile` | профиль пользователя |
| `/dishes/` | `dishes.views.dishes_list` | каталог блюд |
| `/dishes/<int:dish_id>/` | `dishes.views.dish_detail` | карточка блюда |
| `/plan/` | `planner.views.plan_list` | план питания |
| `/plan/<int:meal_id>/` | `planner.views.meal_detail` | карточка приёма |

Отсутствующие URL и несуществующие идентификаторы возвращают
собственную страницу с кодом 404.

### Django-приложения

| Приложение | Назначение |
|---|---|
| `homepage` | главная страница, профиль, каркас `page()` |
| `dishes` | каталог блюд и карточка блюда |
| `planner` | план питания и карточка приёма |

Приложение для пользователя не создаётся: Django предоставляет
встроенную модель `django.contrib.auth.User`. На ПР5 она пока
не задействована — используется наш собственный `UserProfile`.

## Хранение данных

Данные хранятся в JSON-файлах:

- `data/dishes.json` — каталог блюд (с полем `id`);
- `data/plan.json` — план питания;
- `data/user.json` — профиль пользователя.

При загрузке JSON преобразуется в объекты `Dish`, `Meal`,
`UserProfile`. При сохранении — обратно в JSON. Преобразование
выполняет модуль `storage.py`, а не `main.py` и не view-функции.

## Структура проекта

```

meal_planner/
├── README.md
├── requirements.txt
├── pyproject.toml          — настройки mypy
├── pytest.ini              — настройки pytest
├── .flake8                 — настройки flake8
├── manage.py               — управление Django
├── main.py                 — консольная точка входа
├── storage.py              — JSON ↔ объекты
├── utils.py                — даты и ввод
├── models/                 — объектная модель предметной области
│   ├── **init**.py
│   ├── ingredient.py
│   ├── dish.py
│   ├── user.py
│   └── meal.py
├── mealplanner/            — Django-проект
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── homepage/               — Django-приложение: главная, профиль
├── dishes/                 — Django-приложение: каталог блюд
├── planner/                — Django-приложение: план питания
├── data/
│   ├── dishes.json
│   ├── plan.json
│   └── user.json
└── tests/
├── conftest.py
├── test_dish.py
├── test_meal.py
└── test_user.py

```

**Пакет `models/` (наш) и файлы `dishes/models.py`,
`planner/models.py`, `homepage/models.py` (Django)** — это разные
вещи. Пакет `models/` содержит классы предметной области ПР3;
файлы `models.py` Django-приложений пусты и будут заполнены
на ПР7 при переходе на Django ORM.

## Запуск

### Веб-версия

```bash
python manage.py migrate
python manage.py runserver
```

Открыть: http://127.0.0.1:8000/

### Консольная версия (сохранена с ПР3)

```
python main.py
```

## Тесты

```
pytest -v
```

## Проверка стиля

```
flake8 .
```

## Проверка типов

```
mypy .
```

## Текущее состояние и план развития

**Реализовано (ПР5):**

- Django-проект `mealplanner` и три приложения;
- двухуровневая маршрутизация URL через `include()`;
- view-функции и шаблон-каркас `page()` с Bootstrap 5.3;
- страницы каталога, блюда, плана, приёма, профиля;
- обработка ошибки 404;
- работа с данными через модели и `storage.py`.

**Не реализовано (план развития):**

- перенос сущностей в Django ORM (ПР7);
- подключение базы данных вместо JSON;
- переход на шаблоны `templates/` и отказ от `page()` (ПР6);
- Django Forms для создания и редактирования (ПР10);
- аутентификация пользователей (ПР11);
- REST API, контейнеризация, CI/CD.

## Метка коммитов

Коммиты ПР5 начинаются с `PR5:`. Примеры:

```
PR5: add Django project and web pages
PR5: adapt models with id field
PR5: add Django views for dishes and plan
PR5: update README

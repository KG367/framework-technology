"""View-функции приложения planner: план питания и карточка приёма."""

from django.http import HttpRequest, HttpResponse

from homepage.views import page
from models import find_meal_by_id
from storage import load_dishes, load_plan, load_user


def _load_context():
    """Загружает профиль, каталог и план питания пользователя."""
    user = load_user()
    dishes = load_dishes()
    plan = load_plan(dishes, user)
    return user, dishes, plan


def plan_list(request: HttpRequest) -> HttpResponse:
    """Страница со списком приёмов пищи в плане."""
    _user, _dishes, plan = _load_context()
    if not plan:
        content = """
            <h1>План питания</h1>
            <p>План пуст.</p>
        """
        return HttpResponse(page("План питания", content))
    items = ""
    ordered = sorted(plan, key=lambda m: (m.date, m.slot))
    for meal in ordered:
        text = (
            f"{meal.date} — {meal.slot} — "
            f"{meal.dish.name} x{meal.portions}"
        )
        link = f'<a href="/plan/{meal.meal_id}/">{text}</a>'
        items += f'<li class="list-group-item">{link}</li>'
    content = f"""
        <h1>План питания</h1>
        <ul class="list-group">{items}</ul>
    """
    return HttpResponse(page("План питания", content))


def meal_detail(
    request: HttpRequest,
    meal_id: int,
) -> HttpResponse:
    """Страница одного приёма пищи."""
    _user, _dishes, plan = _load_context()
    meal = find_meal_by_id(plan, meal_id)
    if meal is None:
        content = """
            <h1 class="text-danger">Приём пищи не найден</h1>
            <a href="/plan/" class="btn btn-outline-secondary">
                ← к плану питания
            </a>
        """
        return HttpResponse(
            page("Приём пищи не найден", content),
            status=404,
        )
    ingredients = "".join(
        f"<li>{item}</li>" for item in meal.dish.ingredients
    )
    content = f"""
        <div class="card">
            <div class="card-body">
                <h5 class="card-title">
                    Приём пищи №{meal.meal_id}
                </h5>
                <p class="card-text">
                    <strong>Дата:</strong> {meal.date}
                </p>
                <p class="card-text">
                    <strong>Приём:</strong> {meal.slot}
                </p>
                <p class="card-text">
                    <strong>Блюдо:</strong> {meal.dish.name}
                </p>
                <p class="card-text">
                    <strong>Порций:</strong> {meal.portions}
                </p>
                <p class="card-text">
                    <strong>Пользователь:</strong> {meal.user.name}
                </p>
                <p class="card-text">
                    <strong>Ингредиенты:</strong>
                </p>
                <ul>{ingredients}</ul>
                <a href="/plan/" class="btn btn-outline-secondary">
                    ← к плану питания
                </a>
            </div>
        </div>
    """
    return HttpResponse(
        page(f"Приём пищи №{meal.meal_id}", content)
    )

"""View-функции приложения dishes: список блюд и карточка блюда."""

from django.http import HttpRequest, HttpResponse

from homepage.views import page
from models import find_dish_by_id
from storage import load_dishes


def dishes_list(request: HttpRequest) -> HttpResponse:
    """Страница со списком всех блюд."""
    dishes = load_dishes()
    items = ""
    for dish in dishes:
        text = (
            f"{dish.name} — {dish.slot}, "
            f"{dish.minutes} мин, {dish.kcal} ккал"
        )
        link = f'<a href="/dishes/{dish.dish_id}/">{text}</a>'
        items += f'<li class="list-group-item">{link}</li>'
    content = f"""
        <h1>Каталог блюд</h1>
        <ul class="list-group">{items}</ul>
    """
    return HttpResponse(page("Каталог блюд", content))


def dish_detail(
    request: HttpRequest,
    dish_id: int,
) -> HttpResponse:
    """Страница одного блюда."""
    dishes = load_dishes()
    dish = find_dish_by_id(dishes, dish_id)
    if dish is None:
        content = """
            <h1 class="text-danger">Блюдо не найдено</h1>
            <a href="/dishes/" class="btn btn-outline-secondary">
                ← к каталогу блюд
            </a>
        """
        return HttpResponse(
            page("Блюдо не найдено", content),
            status=404,
        )
    ingredients = "".join(
        f"<li>{item}</li>" for item in dish.ingredients
    )
    content = f"""
        <div class="card">
            <div class="card-body">
                <h5 class="card-title">{dish.name}</h5>
                <p class="card-text">
                    <strong>Приём пищи:</strong> {dish.slot}
                </p>
                <p class="card-text">
                    <strong>Время готовки:</strong> {dish.minutes} мин
                </p>
                <p class="card-text">
                    <strong>Калорийность:</strong> {dish.kcal} ккал
                </p>
                <p class="card-text">
                    <strong>Ингредиенты:</strong>
                </p>
                <ul>{ingredients}</ul>
                <a href="/dishes/" class="btn btn-outline-secondary">
                    ← к каталогу блюд
                </a>
            </div>
        </div>
    """
    return HttpResponse(page(dish.name, content))

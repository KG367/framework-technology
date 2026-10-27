"""View-функции приложения dishes: список блюд и карточка блюда."""

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from models import find_dish_by_id
from storage import load_dishes


def dishes_list(request: HttpRequest) -> HttpResponse:
    """Страница со списком всех блюд."""
    dishes = load_dishes()
    context = {"dishes": dishes}
    return render(request, "dishes/dish_list.html", context)


def dish_detail(
    request: HttpRequest,
    dish_id: int,
) -> HttpResponse:
    """Страница одного блюда."""
    dishes = load_dishes()
    dish = find_dish_by_id(dishes, dish_id)
    context = {"dish": dish}
    return render(
        request,
        "dishes/dish_detail.html",
        context,
        status=404 if dish is None else 200,
    )

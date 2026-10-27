"""View-функции приложения planner: план питания и карточка приёма."""

from typing import Tuple, List

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from models import Dish, Meal, UserProfile, find_meal_by_id
from storage import load_dishes, load_plan, load_user


def _load_data() -> Tuple[List[Dish], List[Meal], UserProfile]:
    """Загружает каталог блюд, план питания и профиль пользователя."""
    user = load_user()
    dishes = load_dishes()
    plan = load_plan(dishes, user)
    return dishes, plan, user


def plan_list(request: HttpRequest) -> HttpResponse:
    """Страница со списком приёмов пищи в плане."""
    _dishes, plan, _user = _load_data()
    context = {"plan": plan}
    return render(request, "planner/plan_list.html", context)


def meal_detail(
    request: HttpRequest,
    meal_id: int,
) -> HttpResponse:
    """Страница одного приёма пищи."""
    _dishes, plan, _user = _load_data()
    meal = find_meal_by_id(plan, meal_id)
    context = {"meal": meal}
    return render(
        request,
        "planner/meal_detail.html",
        context,
        status=404 if meal is None else 200,
    )

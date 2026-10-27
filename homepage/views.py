"""View-функции приложения homepage: главная и профиль."""

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from storage import load_user


def index(request: HttpRequest) -> HttpResponse:
    """Главная страница приложения."""
    return render(request, "homepage/index.html")


def profile(request: HttpRequest) -> HttpResponse:
    """Страница профиля пользователя."""
    user = load_user()
    context = {"user": user}
    return render(request, "homepage/profile.html", context)


def page_not_found(
    request: HttpRequest,
    exception: Exception,
) -> HttpResponse:
    """Собственная страница ошибки 404."""
    return render(request, "404.html", status=404)

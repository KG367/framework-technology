"""View-функции главного приложения: каркас страницы, главная, профиль."""

from django.http import HttpRequest, HttpResponse

from storage import load_user


def page(title: str, content: str) -> str:
    """Собирает HTML-страницу с общим каркасом и навигацией."""
    bootstrap = (
        "https://cdn.jsdelivr.net/npm/bootstrap@5.3.3"
        "/dist/css/bootstrap.min.css"
    )
    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport"
          content="width=device-width, initial-scale=1">
    <title>{title}</title>
    <link rel="stylesheet" href="{bootstrap}">
</head>
<body>
<nav class="navbar navbar-expand-lg navbar-dark bg-dark mb-3">
    <div class="container">
        <a class="navbar-brand" href="/">MealPlanner</a>
        <ul class="navbar-nav">
            <li class="nav-item">
                <a class="nav-link" href="/dishes/">Блюда</a>
            </li>
            <li class="nav-item">
                <a class="nav-link" href="/plan/">План</a>
            </li>
            <li class="nav-item">
                <a class="nav-link" href="/profile/">Профиль</a>
            </li>
        </ul>
    </div>
</nav>
<main class="container">{content}</main>
</body>
</html>"""


def index(request: HttpRequest) -> HttpResponse:
    """Главная страница приложения."""
    content = """
        <h1 class="display-4">MealPlanner</h1>
        <p class="lead">
            Система планирования приготовления блюд.
        </p>
        <p>Основные разделы:</p>
        <a href="/dishes/" class="btn btn-primary me-2">Каталог блюд</a>
        <a href="/plan/" class="btn btn-secondary">План питания</a>
    """
    return HttpResponse(page("MealPlanner", content))


def profile(request: HttpRequest) -> HttpResponse:
    """Страница профиля пользователя."""
    user = load_user()
    if user.restrictions:
        restrictions = ", ".join(user.restrictions)
    else:
        restrictions = "нет"
    content = f"""
        <h1>Профиль</h1>
        <ul class="list-group">
            <li class="list-group-item">
                <strong>Имя:</strong> {user.name}
            </li>
            <li class="list-group-item">
                <strong>Цель по калориям:</strong>
                {user.target_kcal} ккал/день
            </li>
            <li class="list-group-item">
                <strong>Бюджет:</strong>
                {user.budget} руб/неделя
            </li>
            <li class="list-group-item">
                <strong>Ограничения:</strong> {restrictions}
            </li>
        </ul>
    """
    return HttpResponse(page("Профиль", content))


def page_not_found(
    request: HttpRequest,
    exception: Exception,
) -> HttpResponse:
    """Собственная страница ошибки 404."""
    content = """
        <h1 class="text-danger">404 — страница не найдена</h1>
        <p>Проверьте адрес или вернитесь на главную.</p>
        <a href="/" class="btn btn-primary">На главную</a>
    """
    return HttpResponse(
        page("404 — страница не найдена", content),
        status=404,
    )

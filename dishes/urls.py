"""Маршруты приложения dishes: список блюд и карточка блюда."""

from django.urls import path

from . import views

app_name = "dishes"

urlpatterns = [
    path("", views.dishes_list, name="list"),
    path("<int:dish_id>/", views.dish_detail, name="detail"),
]

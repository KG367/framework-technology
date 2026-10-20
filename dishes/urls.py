"""Маршруты приложения dishes: список блюд и карточка блюда."""

from django.urls import path

from . import views

urlpatterns = [
    path("", views.dishes_list, name="dishes_list"),
    path("<int:dish_id>/", views.dish_detail, name="dish_detail"),
]

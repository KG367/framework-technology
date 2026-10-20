"""Маршруты приложения planner: план питания и карточка приёма."""

from django.urls import path

from . import views

urlpatterns = [
    path("", views.plan_list, name="plan_list"),
    path("<int:meal_id>/", views.meal_detail, name="meal_detail"),
]

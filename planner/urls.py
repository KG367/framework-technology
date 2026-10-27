"""Маршруты приложения planner: план питания и карточка приёма."""

from django.urls import path

from . import views

app_name = "planner"

urlpatterns = [
    path("", views.plan_list, name="list"),
    path("<int:meal_id>/", views.meal_detail, name="detail"),
]

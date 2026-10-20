"""Корневая конфигурация маршрутов Django-проекта mealplanner."""

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("homepage.urls")),
    path("dishes/", include("dishes.urls")),
    path("plan/", include("planner.urls")),
]

handler404 = "homepage.views.page_not_found"

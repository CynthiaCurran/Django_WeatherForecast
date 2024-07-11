from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("weather_query/", views.weather_query, name="weather_query"),
]
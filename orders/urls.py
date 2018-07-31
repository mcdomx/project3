from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("register", views.register, name="register"),
    path("get_menu_items", views.get_menu_items, name="get_menu_items"),
    path("get_toppings", views.get_toppings, name="get_toppings"),
    path("place_order", views.place_order, name="place_order"),
]

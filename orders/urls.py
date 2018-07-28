from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("register", views.register, name="register"),
    path("get_menu_items", views.get_menu_items, name="get_menu_items"),
    path("get_toppings", views.get_toppings, name="get_toppings"),
    path("get_sub_options", views.get_sub_options, name="get_sub_options")
]

from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("register", views.register, name="register"),
    path("get_menu_items", views.get_menu_items, name="get_menu_items")
    # url(r'^register/$', orders_views.register, name='register'),
]

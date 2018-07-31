from django.contrib import admin
from .models import Menu_categories, Menu_items, Sub_addons, Order, Order_line, Pizza_toppings, Sizes, Toppings

# Register your models here.
admin.site.register(Menu_categories)
admin.site.register(Menu_items)
admin.site.register(Sub_addons)
admin.site.register(Order)
admin.site.register(Order_line)
admin.site.register(Pizza_toppings)
admin.site.register(Sizes)
admin.site.register(Toppings)

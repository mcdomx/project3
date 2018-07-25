from django.contrib import admin
from .models import Menu_categories, Menu_items, Sub_addons

# Register your models here.
admin.site.register(Menu_categories)
admin.site.register(Menu_items)
admin.site.register(Sub_addons)

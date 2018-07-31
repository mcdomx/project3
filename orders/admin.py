from django.contrib import admin
from .models import Menu_categories, Menu_items, Sub_addons, Order, Order_line, Pizza_toppings, Sizes, Toppings

# Register your models here.
admin.site.register(Menu_categories)
# admin.site.register(Menu_items)
admin.site.register(Sub_addons)
# admin.site.register(Order)
admin.site.register(Order_line)
admin.site.register(Pizza_toppings)
admin.site.register(Sizes)
admin.site.register(Toppings)

# Define the admin class
# class Menu_itemsInstanceInline(admin.TabularInline):
#     model = Menu_itemsInstance

class Menu_itemsAdmin(admin.ModelAdmin):
    list_display = ('id', 'category', 'item', 'size', 'toppings', 'price', 'available')
    list_filter = ('category', 'available')
    # inlines = [Menu_itemsInstance]

# Register the admin class with the associated model
admin.site.register(Menu_items, Menu_itemsAdmin)

class Order_lineInline(admin.TabularInline):
    model = Order_line
    fk_name = "order"

class OrderAdmin(admin.ModelAdmin):
    inlines = [
        Order_lineInline,
    ]

admin.site.register(Order, OrderAdmin)

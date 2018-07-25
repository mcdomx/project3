from django.db import models


# menu_categories
class Menu_categories(models.Model):
    category = models.CharField(primary_key = True, max_length = 64)
    available = models.BooleanField(default = True)

    def __str__(self):
        return f'{self.category}'

# menu_items
class Menu_items(models.Model):
    SIZE_CHOICES = (
     ('SM', 'small'),
     ('LG', 'large')
    )

    TOPPINGS_CHOICES = (
        ('CHEESE', 'cheese'),
        ('1', '1 topping' ),
        ('2', '2 toppings' ),
        ('3', '3 toppings' ),
        ('SPECIAL', 'special')
    )

    item = models.CharField(max_length = 64, blank = False)
    category = models.ForeignKey(Menu_categories, on_delete = models.CASCADE, blank = False, default="None", related_name="items")
    allow_sub_addons = models.BooleanField(default=False)
    available = models.BooleanField(default=True)
    size = models.CharField(max_length = 16, choices = SIZE_CHOICES, blank = False)
    toppings = models.CharField(max_length = 64, choices = TOPPINGS_CHOICES, blank = False)
    price = models.DecimalField(blank = False, max_digits=5, decimal_places=2, default=0.00)

    def __str__(self):
        if self.size == '':
            return f'{self.category} : {self.item}  {self.get_toppings_display()}'
        else:
            return f'{self.category} : {self.item}  ({self.size})  {self.get_toppings_display()}'

# # sub_addons
class Sub_addons(models.Model):
    SIZE_CHOICES = (
     ('SM', 'small'),
     ('LG', 'large')
    )

    add_on = models.CharField(max_length = 64, blank = False)
    size = models.CharField(max_length = 16, choices = SIZE_CHOICES, blank = False)
    available = models.BooleanField(default = True)
    restricted_menu_item = models.CharField(max_length = 64, blank = False)
    price = models.DecimalField(blank = False, max_digits=5, decimal_places=2, default=0.00)

    def __str__(self):
        return f'{self.add_on} ({self.size})'







# class Airport(models.Model):
#     code = models.CharField(max_length = 3)
#     city = models.CharField(max_length = 64)
#
#     def __str__(self):
#         return f"{self.city} ({self.code})"
#
# class Flight(models.Model):
#     origin = models.ForeignKey(Airport, on_delete = models.CASCADE, related_name="departures")
#     destination = models.ForeignKey(Airport, on_delete = models.CASCADE, related_name="arrivals")
#     duration = models.IntegerField()
#
#     def __str__(self):
#         return f"{self.id} - {self.origin} to {self.destination}"
#
# class Passenger(models.Model):
#     first = models.CharField(max_length = 64)
#     last = models.CharField(max_length = 64)
#     flights = models.ManyToManyField(Flight, blank = True, related_name = "passengers")
#
#     def __str__(self):
#         return f"{self.first} {self.last}"

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

    item = models.CharField(max_length = 64)
    category = models.ForeignKey(Menu_categories, on_delete = models.CASCADE, default="None", related_name="items")
    allow_sub_addons = models.BooleanField(default=False)
    available = models.BooleanField(default=True)
    size = models.CharField(max_length = 16, choices = SIZE_CHOICES)
    toppings = models.CharField(max_length = 64, choices = TOPPINGS_CHOICES)
    price = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)

    def get_item(item, size, toppings):
        try:
            rv = Menu_items.objects.get(item=item, size=size, toppings=toppings)
        except Menu_items.DoesNotExist:
            return "Item doesn't exist in menu"
        except MultipleObjectsReturned:
            return "More than one such item exists in the menu"

        return rv

    def get_price(self):
        return self.price

    def as_dict(self):
        rv = vars(self)
        del rv['_state']
        return rv


    def get_varval(self, variable):
        return self.variable

    # def __str__(self):
    #     if self.size == '':
    #         return f'{self.category} : {self.item}  {self.get_toppings_display()}'
    #     else:
    #         return f'{self.category} : {self.item}  ({self.size})  {self.get_toppings_display()}'

# sub_addons
class Sub_addons(models.Model):
    SIZE_CHOICES = (
     ('SM', 'small'),
     ('LG', 'large')
    )

    add_on = models.CharField(max_length = 64)
    size = models.CharField(max_length = 16, choices = SIZE_CHOICES)
    available = models.BooleanField(default = True)
    restricted_menu_item = models.CharField(max_length = 64)
    price = models.DecimalField(blank = False, max_digits=5, decimal_places=2, default=0.00)

    def get_price(add_on):
        return Sub_addons.objects(add_on=add_on).price

    def as_dict(self):
        rv = vars(self)
        del rv['_state']
        return rv

    # def __str__(self):
    #     return f'{self.add_on} ({self.size})'

# toppings
class Pizza_toppings(models.Model):
    topping = models.CharField(max_length = 64, blank = False)
    available = models.BooleanField(default = True)

    # def is_available(topping):
    #     return Pizza_toppings.objects(topping=topping).available

    def __str__(self):
        return f'{self.topping}'

    def as_list():
        rv = []
        full_list = Pizza_toppings.objects.all()
        for t in full_list:
            if t.available is True:
                rv.append(t.topping)
        return rv
        # for variable in vars(self):
        #     rv[variable] = variable



# order line
class Order_line(models.Model):
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

    item = models.ForeignKey(Menu_items, on_delete = models.CASCADE, blank = True, null = True)
    # category = models.ForeignKey(Menu_categories, on_delete = models.CASCADE, blank = True, null = True)
    size = models.CharField(max_length = 16, choices = SIZE_CHOICES, blank = True)
    toppings = models.CharField(max_length = 64, choices = TOPPINGS_CHOICES, blank = True)
    topping_items = models.ManyToManyField(Pizza_toppings, blank = True)
    sub_addons = models.ManyToManyField(Sub_addons, blank = True)
    price = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)

    def add_topping(self, topping):
        self.topping_items.add(topping)
        update_toppings(self)

    def remove_topping(self, topping):
        self.topping_items.remove(topping)
        update_toppings(self)

    def update_toppings(self):
        num_toppings = self.topping_items.objects.count()
        if num_toppings == 1:
            self.toppings = "CHEESE"
        elif num_toppings == 2:
            self.toppings = "1"
        elif num_toppings == 3:
            self.toppings = "2"
        elif num_toppings == 4:
            self.toppings = "3"
        else:
            num_toppings = "SPECIAL"

    def add_sub_addon(self, sub_addon):
        self.sub_addons.add(sub_addon)

    def remove_sub_addon(self, sub_addon):
        r = self.objects.filter(sub_addon=sub_addon)
        self.sub_addons.remove(r)

    def change_size(self, size):
        self.size = size

    # calculate the total price of the line
    def update_price(self):
        # self.price = Menu_items.get_item(self.menu_item, self.size, self.toppings).get_price()
        self.price = Menu_items.objects.get(item=self.item, size=self.size, toppings=self.toppings)
        for addon in self.sub_addons:
            self.price += Sub_addons.get_price(addon)

    def get_price(self):
        return self.price

    def remove_line(self, order):
        order.lines.remove(self)
        Order_line.objects.filter(id=self.id).delete()
        self.delete()

    # def save(self, *args, **kwargs):
    #     Order_line.update_price(self)

    def __str__(self):
        op_string = f"{self.item} ({self.size}) ${self.price}"
        return op_string


# order
class Order(models.Model):

    date = models.DateTimeField(auto_now=True)
    lines = models.ManyToManyField(Order_line)
    price = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)

    # calculate the total price of the order
    def update_order_price(self):
        price = 0
        for l in self.lines:
            price += l.price



# Customer
# class Customer(models.Model):



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

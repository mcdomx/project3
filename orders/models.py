from django.db import models


# menu_categories
class Menu_categories(models.Model):
    category = models.CharField(primary_key = True, max_length = 64)
    available = models.BooleanField(default = True)

    def __str__(self):
        return f'{self.category}'

class Sizes (models.Model):
    size = models.CharField(primary_key=True, max_length = 16)
    description = models.CharField(max_length = 64)

    def __str__(self):
        return f'{self.size}-{self.description}'

class Toppings (models.Model):
    option = models.CharField(primary_key=True, max_length = 16)
    description = models.CharField(max_length = 64)

# sub_addons
class Sub_addons(models.Model):

    id = models.AutoField(primary_key = True)
    add_on = models.CharField(max_length = 64)
    size = models.ForeignKey(Sizes, on_delete = models.CASCADE)
    available = models.BooleanField(default = True)
    price = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)

    def get_price(add_on):
        return Sub_addons.objects(add_on=add_on).price

    def as_dict(self):
        rv = vars(self)
        del rv['_state']
        return rv



    # def __str__(self):
    #     return f'{self.add_on} ({self.size})'

# menu_items
class Menu_items(models.Model):

    # TOPPINGS_CHOICES = (
    #     ('CHEESE', 'cheese'),
    #     ('1', '1 topping' ),
    #     ('2', '2 toppings' ),
    #     ('3', '3 toppings' ),
    #     ('SPECIAL', 'special'),
    #     ('NA', 'no toppings')
    # )

    id = models.AutoField(primary_key=True)
    item = models.CharField(max_length = 64)
    category = models.ForeignKey(Menu_categories, on_delete = models.CASCADE)
    size = models.ForeignKey(Sizes, on_delete = models.CASCADE, blank = True, null = True)
    toppings = models.ForeignKey(Toppings, on_delete = models.CASCADE, blank = True, null = True)
    addons = models.ManyToManyField(Sub_addons, blank = True)
    available = models.BooleanField(default=True)
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
        rv = {}
        rv["category"] = self.category.category
        rv["item"] = self.item
        rv["size"] = self.size.description
        if self.category.category is "Pizza":
            rv["toppings_desc"] = self.toppings.description
        rv["price"] = self.price
        return rv


    def get_varval(self, variable):
        return self.variable

    # def __str__(self):
    #     if self.size == '':
    #         return f'{self.category} : {self.item}  {self.get_toppings_display()}'
    #     else:
    #         return f'{self.category} : {self.item}  ({self.size})  {self.get_toppings_display()}'



# toppings
class Pizza_toppings(models.Model):
    topping = models.CharField(max_length = 64, blank = False)
    available = models.BooleanField(default = True)

    def __str__(self):
        return f'{self.topping}'

    def as_list():
        rv = []
        full_list = Pizza_toppings.objects.all()
        for t in full_list:
            if t.available is True:
                rv.append(t.topping)
        return rv




# order line
class Order_line(models.Model):
    SIZE_CHOICES = (
     ('SM', 'small'),
     ('LG', 'large'),
     ('NA', 'one size')
    )

    TOPPINGS_CHOICES = (
        ('CHEESE', 'cheese'),
        ('1', '1 topping' ),
        ('2', '2 toppings' ),
        ('3', '3 toppings' ),
        ('SPECIAL', 'special'),
        ('NA', 'no toppings')
    )

    line_num = models.IntegerField()
    item = models.ForeignKey(Menu_items, on_delete = models.CASCADE, blank = True, null = True)
    category = models.ForeignKey(Menu_categories, on_delete = models.CASCADE, blank = True, null = True)
    size = models.CharField(max_length = 16, choices = SIZE_CHOICES, blank = True, null = True)
    toppings = models.CharField(max_length = 64, choices = TOPPINGS_CHOICES, blank = True, null = True)
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

    order_num = models.AutoField(primary_key=True)
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

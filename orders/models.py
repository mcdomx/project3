from django.db import models


# notes from class
# from django.http import JSONResponse
# response = JsonResponse(someDictinoary)  # use safe=False to return list


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

    def get_item(menu_item, size, toppings):
        return Menu_items.objects(menu_item=menu_item, size=size, toppings=toppings).first()

    def __str__(self):
        if self.size == '':
            return f'{self.category} : {self.item}  {self.get_toppings_display()}'
        else:
            return f'{self.category} : {self.item}  ({self.size})  {self.get_toppings_display()}'

# sub_addons
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

    def get_price(add_on):
        return Sub_addons.objects(add_on=add_on).price

    def __str__(self):
        return f'{self.add_on} ({self.size})'

# order
class Order(models.Model):

    def __init__(self):
        #let order number be auto generated
        self.date = models.DateTimeField(auto_now=True)
        self.lines = () #ordered list of order order_lines
        self.price = () #tuple with total price and a description of the subtotal

    # calculate the total price of the order
    def update_order_price(self):
        price = 0
        for l in self.lines:
            price += l.price


# order line
class Order_line(models.Model):

    # toppings is an ordered list of items from toppings table
    # sub_addons is an order list of items from sub_addons table
    def __init__(self, order, menu_item, size):
        self.menu_item = menu_item
        self.size = size
        self.toppings = "CHEESE"
        self.topping_tems = []
        self.sub_addons = {}
        self.price = update_price(self)
        order.lines.append(self)

    def add_topping(self, topping):
        self.topping_items.append(topping)
        update_toppings(self)

    def remove_topping(self, topping):
        self.toppings.remove(topping)
        update_toppings(self)

    def update_toppings(self):
        num_toppings = len(self.topping_items)
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

        self.sub_addons.append(sub_addon)

    def remove_sub_addon(self, sub_addon):
        self.sub_addons.remove(sub_addon)

    def change_size(self, size):
        self.size = size

    # calculate the total price of the line
    def update_price(self):
        self.price = Menu_items.get_items(self.menu_item, self.size, self.toppings).price

    def get_price(self):
        return self.price

    def remove_line(self, order):
        order.lines.remove(self)
        Order_line.objects.filter(id=self.id).delete()
        self.delete()
        # no need to delete self object in Python since no reference to self
        # object will automatically be garbage collected in Python

    def __str__(self):
        op_string = self.menu_item
        if self.size is not '':
            op_string += f' ({self.size})'
        if self.toppings is not '':
            op_string += f' ({self.toppings})'
            for t in self.topping_items:
                op_string += f'\r\t+{t}'
            op_string += f'\t'
        if self.sub_addons is not '':
            for s in self.sub_addons:
                op_string += f'\r\t+{s} \t+${Sub_addons.get_price(s)}'
        op_string += f'\t\t+${self.price}'
        return op_string

        # this will be what is printed on the receipt / order summary
        # examples:
        # Line 1: Regular Pizza (LG) 1 Topping
        #             +Onions                                $0.00

        # Line 2: Steak + Cheese (LG)             $0.00
        #            +Mushrooms                  +$0.00
        #            +Peppers                    +$0.00      $0.00

        # Line 3: Baked Ziti w/Meatballs                     $0.00


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

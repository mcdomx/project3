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

    def __str__(self):
        return f'{self.add_on} ({self.size})'

# order
class Order(models.Model):

    #let order number be auto generated
    order_date = models.DateTimeField(auto_now=True)
    order_lines = () #ordered list of order order_lines
    price = () #tuple with total price and a description of the subtotal

    # calculate the total price of the order
    def_calc_order_price(self):

# order line
class Order_line(models.Model):

    # toppings is an ordered list of items from toppings table
    # sub_addons is an order list of items from sub_addons table
    def __init__(self, menu_item, size, toppings, sub_addons):
        self.menu_item = menu_item
        self.size = size

        # ensure that toppings is a list
        if type(topping) is not tuple
            self.toppings = (toppings)
        else
            self.toppings = toppings

        # ensure that sub_addons is a list
        if type(sub_addons) is not tuple
            self.sub_addons = (sub_addons)
        else
            self.sub_addons = sub_addons

        order.order_lines.append(self)

    def add_topping(self, topping):
        self.toppings.append(topping)

    def remove_topping(self, topping):
        self.toppings.remove(topping)

    def add_sub_addon(self, sub_addon):
        self.sub_addons.append(sub_addon)

    def remove_sub_addon(self, sub_addon):
        self.sub_addons.remove(sub_addon)

    def change_size(self, size):
        self.size = size

    def __str__(self):
        op_string = self.menu_item
        if size in not '':
            op_string += f' ({self.size})'
        if toppings
        # this will be what is printed on the receipt / order summary
        # examples:
        # Line 1: Regular Pizza (LG) 1 Topping:
        #           Cheese                                  $$$$$
        # Line 2: Sub: Steak + Cheese (LG):
        #            Mushrooms +$0.00
        #            Peppers +$0.00                         $$$$$
        # Line 3: Pasta: Baked Ziti w/Meatballs             $$$$$

    # calculate the total price of the line
    def calc_line_price(self):
        # this needs to be dynamoc in case new categories are added
        # find base price
        # if addons exist, add the price of addons
        # return a tuple with the price and a long description of the details



    # notes from class
    from django.http import JSONResponse
    response = JsonResponse(someDictinoary)  # use safe=False to return list

    def add_item(self):




# Customer
class Customer(models.Model):



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

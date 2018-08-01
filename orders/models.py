from django.db import models
from django.contrib.auth.models import User


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

    def __str__(self):
        return f'{self.description}'

# sub_addons
class Sub_addons(models.Model):

    id = models.AutoField(primary_key = True)
    addon = models.CharField(max_length = 64)
    size = models.ForeignKey(Sizes, on_delete = models.CASCADE)
    available = models.BooleanField(default = True)
    price = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)

    def as_dict(self):
        rv = {}
        for a in self:
            rv[self.addon] = self.price
        return rv

    def __str__(self):
        return f'{self.addon} ({self.size}) ${self.price}'

# menu_items
class Menu_items(models.Model):

    id = models.AutoField(primary_key=True)
    item = models.CharField(max_length = 64)
    category = models.ForeignKey(Menu_categories, on_delete = models.CASCADE)
    size = models.ForeignKey(Sizes, on_delete = models.CASCADE, blank = True, null = True)
    toppings = models.ForeignKey(Toppings, on_delete = models.CASCADE, blank = True, null = True)
    addons = models.ManyToManyField(Sub_addons, blank = True)
    available = models.BooleanField(default=True)
    price = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)

    def __str__(self):
        rv = f"{self.category}:{self.item}"
        if (self.size.size != "NA"):
            rv += f" ({self.size.size})"
        if (self.toppings.option != "NA"):
            rv += f" ({self.toppings.option})"
        rv += f" ${self.price}"
        if (self.available == False):
            rv += " UNAVAILABLE"
        return rv

    def as_dict(self):
        # turn addons into a dict
        avail_addons = self.addons.all()
        a_dict = {}
        for a in avail_addons:
            a_dict[a.addon] = a.price

        rv = {}
        rv["category"] = self.category.category
        rv["item"] = self.item
        rv["size"] = self.size.size
        rv["toppings_opt"] = self.toppings.option
        rv["toppings_desc"] = self.toppings.description
        rv["addons"] = a_dict
        rv["price"] = self.price
        return rv


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


#order status'
class Order_status(models.Model):
    status = models.CharField(primary_key=True, max_length = 64, blank = False)

    def __str__(self):
        return f'{self.status}'

# order
class Order(models.Model):
    date = models.DateTimeField(auto_now=True)
    customer = models.ForeignKey(User, on_delete = models.CASCADE, blank=True, null=True)
    status = models.ForeignKey(Order_status, on_delete = models.CASCADE, default="placed")
    price = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)

    # def __str__(self):
    #     return f'Order Number:{self.id} Price:${self.price}'

    def as_dict(self):
        rv = {
            "id": self.id,
            "date": self.date,
            "customer": self.customer.get_username(),
            "status": self.status.status,
            "price": self.price
        }
        return rv


# order line
class Order_line(models.Model):

    line_num = models.IntegerField()
    order = models.ForeignKey(Order, on_delete = models.CASCADE, blank = True, null = True, related_name="lines")
    item = models.ForeignKey(Menu_items, on_delete = models.CASCADE, blank = True, null = True)
    topping_items = models.ManyToManyField(Pizza_toppings, blank = True)
    addons = models.ManyToManyField(Sub_addons, blank = True)
    price = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)

    def create(self, line_num, line, order):
        size_obj = Sizes.objects.get(size=line['size'])
        top_obj = Toppings.objects.get(option=line['toppings_opt'])
        order_obj = Order.objects.get(id=order.id)

        self.line_num = line_num
        self.order = order
        self.save()
        self.item = Menu_items.objects.get(item=line['item'], category_id=line['category'], size=size_obj, toppings=top_obj)

        for t in line['toppings_list']:
            tobj = Pizza_toppings.objects.get(topping=t)
            self.topping_items.add(tobj)
        for s in line['sub_options_list']:
            aobj = Sub_addons.objects.get(addon=s, size=self.item.size)
            self.addons.add(aobj)

        self.price = line['total_line_price']
        self.save()


    def __str__(self):
        op_string = f"{self.line_num}: ({self.item}) ${self.price}"
        return op_string

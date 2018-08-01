from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from orders.forms import RegistrationForm
from .models import Menu_items, Pizza_toppings, Sub_addons, Sizes, Toppings, Order, Order_line, Order_status
from django.http import JsonResponse

from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm

import json

# render main landing page of site
def index(request):
    menu_items = Menu_items.objects.values('category','item').distinct()
    context = {'menu_items': menu_items,}
    return render(request, "orders/index.html", context)


# render order maintenance page with list of orders that are not complete
def order_maint(request):
    context = {}
    context["orders"] = Order.objects.exclude(status='complete')
    context["statuses"] = Order_status.objects.all()
    return render(request, "orders/order_maint.html", context)


# render the register page with secure registration form
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        form = RegistrationForm()
    return render(request, 'orders/register.html', {'form': form})



# get menu items based on data in form
# many items may be returned or a single item
def get_menu_items(request):

    item= request.POST.get("sel_item")
    category = request.POST.get("sel_cat")
    sel_size= request.POST.get("sel_size")
    sel_toppings_list= request.POST.get("sel_toppings_list")
    sel_subOptions= request.POST.get("sel_subOptions")

    if str(category) in "Pizza":
        sel_toppings = sel_toppings_list.split(",")
        if sel_toppings[0] == '':
            option = "CHEESE"
        elif len(sel_toppings) > 3:
            option = "SPECIAL"
        else:
            option = len(sel_toppings)
    else:
        option = 'NA'

    if str(category) in "Pasta" or str(category) in "Salad":
        sel_size='NA'

    size = Sizes.objects.get(size=sel_size)
    topping = Toppings.objects.get(option=option)
    menu_item = Menu_items.objects.get(category=category, item=item, size=size, toppings=topping)

    return JsonResponse(menu_item.as_dict())


# get the avaialble toppings list
def get_toppings(request):
    p_toppings = Pizza_toppings.objects.filter(available=True)
    response = Pizza_toppings.as_list()
    return JsonResponse(response, safe=False)


# place new order and save to databse
def place_order(request):
    order_JSON = request.POST.get("cart");
    order = json.loads(order_JSON)

    # create new order
    new_order = Order()
    new_order.price = order['order_total']
    new_order.customer = request.user
    new_order.save()

    lines = order['order_lines']
    line_num = 1;
    for line in lines:
        new_line = Order_line()
        new_line.create(line_num, line, new_order)
        line_num += 1

    context = {
        'success': True,
        'order_number': new_order.id,
        'order_total': new_order.price
    }

    request.session['cart'] = None;

    return JsonResponse(context)


# change the status of order_num to new_status
def change_status(request):
    order_num = request.POST.get("order_num");
    new_status = request.POST.get("new_status");

    order = Order.objects.get(id=order_num)
    order.status = Order_status.objects.get(status=new_status)
    order.save()

    context = {
        'order': order.as_dict(),
    }

    return JsonResponse(context)

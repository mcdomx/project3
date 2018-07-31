from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from orders.forms import RegistrationForm
from .models import Menu_items, Pizza_toppings, Sub_addons, Sizes, Toppings
from django.http import JsonResponse

import json

# Create your views here.
def index(request):

    menu_items = Menu_items.objects.values('category','item').distinct()

    context = {
        'menu_items': menu_items,
    }
    return render(request, "orders/index.html", context)


# Use session to store shopping cart?
# Session data is in the 'reguest' object as request.session
# You can add something to the session dictionary: request.session['shoppingcart'] = order


from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm

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

    print(f"from form. category: {category}")
    print(f"from form. sel_item: {item}")
    print(f"from form. sel_size: {sel_size}")
    print(f"from form. sel_toppings_list: {sel_toppings_list}")
    print(f"from form. sel_subOptions: {sel_subOptions}")
    size = Sizes.objects.get(size=sel_size)
    topping = Toppings.objects.get(option=option)
    menu_items = Menu_items.objects.filter(category=category, item=item, size=size, toppings=topping)
    for m in menu_items:
        print(m.price)
        print(m.size.size)

    response = []
    # make each item in the query result a dictionary object and add to response
    for obj in menu_items:
        response.append(obj.as_dict())
    print (response)
    return JsonResponse(response, safe=False)


def get_toppings(request):
    p_toppings = Pizza_toppings.objects.filter(available=True)
    response = Pizza_toppings.as_list()

    return JsonResponse(response, safe=False)

def get_sub_options(request):

    sel_item = request.POST.get("sel_item")
    sel_size = request.POST.get("sel_size")
    sel_cat = request.POST.get("sel_cat")

    # get the menu_item and see if it offers sub options and extended options
    item =  Menu_items.objects.get(category=sel_cat, item=sel_item, size=sel_size)
    print(f"from get sub_options item: {item.addons}")
    addons = item.addons #available addons for item selected

    # create a list of dictionary items for response
    response = []
    for obj in addons:
        response.append(obj.as_dict())

    return JsonResponse(response, safe=False)


def place_order(request):
    order = request.POST.get("cart");
    # loop through items and add to a new order



# notes from class
# from django.http import JsonResponse
# response = JsonResponse(someDictinoary)  # use safe=False to return list

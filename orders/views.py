from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from orders.forms import RegistrationForm
from .models import Menu_items, Pizza_toppings, Sub_addons, Sizes
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
    sel_toppings= request.POST.get("sel_toppings")
    sel_subOptions= request.POST.get("sel_subOptions")

    sel_toppings = sel_toppings.split(",")
    print (sel_toppings)
    if str(category) in "Pizza":
        if sel_toppings[0] == '':
            sel_toppings = "CHEESE"
        elif len(sel_toppings) > 3:
            sel_toppings = "SPECIAL"
        else:
            sel_toppings = len(sel_toppings)
    else:
        sel_toppings = ''

    if str(category) in "Pasta" or str(category) in "Salad":
        sel_size=''

    print(f"from form. category: {category}")
    print(f"from form. sel_item: {item}")
    print(f"from form. sel_size: '{sel_size}'")
    print(f"from form. sel_toppings: {sel_toppings}")
    print(f"from form. sel_subOptions: {sel_subOptions}")
    size = Sizes.objects.get(size=sel_size)


    menu_items = Menu_items.objects.filter(category=category, item=item, size=size, toppings=sel_toppings)
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
    response = []
    sel_item = request.POST.get("sel_item")
    sel_size = request.POST.get("sel_size")
    sel_cat = request.POST.get("sel_cat")

    # get the menu_item and see if it offers sub options and extended options
    item =  Menu_items.objects.filter(category=sel_cat, item=sel_item, size=sel_size).first()
    addons = item.allow_sub_addons
    ext_addons = item.extended_addons

    # get the sub addons from the sub_addons table
    if (ext_addons):
        s_options = Sub_addons.objects.filter(available=True, size=sel_size)
    else:
        s_options = Sub_addons.objects.filter(available=True, size=sel_size, extended_addon=False)



    s_options = Sub_addons.objects.filter(available=True, restricted_menu_item='', size=sel_size)

    # create a list of dictionary items for response
    for obj in s_options:
        response.append(obj.as_dict())

    # find any sub options that are restricted to the item selected
    # append them to the response
    s_options_restricted = Sub_addons.objects.filter(available=True, restricted_menu_item=sel_item, size=sel_size)
    if (s_options_restricted):
        for obj in s_options_restricted:
            response.append(obj.as_dict())


    return JsonResponse(response, safe=False)


def place_order(request):
    order = request.POST.get("cart");
    # loop through items and add to a new order



# notes from class
# from django.http import JsonResponse
# response = JsonResponse(someDictinoary)  # use safe=False to return list

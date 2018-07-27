from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from orders.forms import RegistrationForm
from .models import Menu_items, Pizza_toppings
from django.http import JsonResponse

import json

# Create your views here.
def index(request):
    # return HttpResponse("Project 3: TODO")
    # return HttpResponseRedirect(reverse("index"))

    menu_items = Menu_items.objects.values('item').distinct()

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


def get_menu_items(request):

    sel_item= request.POST.get("sel_item")

    menu_items = Menu_items.objects.filter(item=sel_item)
    response = []
    # make each item in the query result a dictionary object and add to response
    for obj in menu_items:
        response.append(obj.as_dict())
    return JsonResponse(response, safe=False)

def get_toppings(request):
    p_toppings = Pizza_toppings.objects.filter(available=True)
    # response = Pizza_toppings.as_dict()
    response = Pizza_toppings.as_list()

    return JsonResponse(response, safe=False)




# notes from class
# from django.http import JsonResponse
# response = JsonResponse(someDictinoary)  # use safe=False to return list

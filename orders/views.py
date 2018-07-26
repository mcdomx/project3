from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from orders.forms import RegistrationForm

# Create your views here.
def index(request):
    # return HttpResponse("Project 3: TODO")
    # return HttpResponseRedirect(reverse("index"))
    context = {}
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

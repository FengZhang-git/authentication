from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
import sys
sys.path.append("..")
from orders.models import Food, Type

# Create your views here.

def index(request):
    if not request.user.is_authenticated:
        # return render(request, "users/login.html", {"message": None})
        return render(request, "users/register.html", {"message": None})

    context = {
        "user": request.user,
        "Regular_Pizza": Food.objects.filter(type=Type.objects.get(name="Regular Pizza")),
        "Sicilian_Pizza": Food.objects.filter(type=Type.objects.get(name="Sicilian Pizza")),
        "Topping": Food.objects.filter(type=Type.objects.get(name="Topping")),
        "Sub": Food.objects.filter(type=Type.objects.get(name="Sub")),
        "Pasta": Food.objects.filter(type=Type.objects.get(name="Pasta")),
        "Salad": Food.objects.filter(type=Type.objects.get(name="Salad")),
        "Dinner_Platter": Food.objects.filter(type=Type.objects.get(name="Dinner Platter")),
        # "foods": Food.objects.all()
    }


    # context = {
    #     "user": request.user,
    #
    #     # "foods": Food.objects.all()
    # }

    return render(request, "orders/menu.html", context)

def register_view(request):
    username = request.POST["username"]
    email = request.POST["email"]
    password = request.POST["password"]
    usertmp = User.objects.filter(username=username)
    if usertmp :
        return render(request, "users/register.html", {"message": "Username has existed."})
    user = User.objects.create_user(username, email, password)
    user.first_name = username
    user.save()
    return render(request, "users/login.html", {"message": None})

def logining_view(request):
    return render(request, "users/login.html", {"message": None})

def login_view(request):
    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "users/login.html", {"message": "Usename or password is wrong."})

def logout_view(request):
    logout(request)
    return render(request, "users/login.html", {"message": "Logged out."})

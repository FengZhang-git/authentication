from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django.urls import reverse
import stripe
from .myemail import SendaEmail
# Create your views here.

from .models import Food, Type, Order



def food(request, food_id):
    try:
        food = Food.objects.get(pk=food_id)

    except Food.DoesNotExist:
        raise Http404("Food does not exist")
    type = Type.objects.get(pk=food.type.id)
    context = {
        "food": food,
        "type": type
    }
    return render(request, "orders/food.html", context)

def order(request, food_id):
    try:
        number = int(request.POST["number"])
        food = Food.objects.get(pk=food_id)
        user = request.user
    # except KeyError:
    #     return render(request, "orders/error.html", {"message": "No selection."})
    except Food.DoesNotExist:
        return render(request, "orders/error.html", {"message": "No food."})
    total = number * food.price
    total = float('%.2f' % total)
    order = Order(user=user, food=food, number=number,total=total)
    order.save()
    if "topping" in food.name or "item" in food.name:
        topping_count = int(food.name[0])
        context = {
            "topping_count": topping_count,
            "Toppings": Food.objects.filter(type = Type.objects.get(name="Topping"))
        }
        return render(request, "orders/topping.html", context)

    if "Special" == food.name:
        topping_count = 5
        context = {
            "topping_count": topping_count,
            "Toppings": Food.objects.filter(type = Type.objects.get(name="Topping"))
        }
        return render(request, "orders/topping.html", context)
    return HttpResponseRedirect(reverse("index"))

def ordertopping(request):
    txt = request.POST["order"]
    # return render(request, "orders/error.html", {"message": txt})
    food_id = []
    tmp = ""
    for t in txt:
        if t == '"':
            continue
        if t != " ":
            tmp +=t
        else:
            food_id.append(int(tmp))
            tmp = ""
    for id in food_id:
        try:
            number = 1
            food = Food.objects.get(pk=id)
            user = request.user
        # except KeyError:
        #     return render(request, "orders/error.html", {"message": "No selection."})
        except Food.DoesNotExist:
            return render(request, "orders/error.html", {"message": "No food."})
        total = 0
        order = Order(user=user, food=food, number=number,total=total)
        order.save()
    return HttpResponseRedirect(reverse("index"))

def cart(request):
    user = request.user
    currentOrders = user.hasorders.filter(is_paid=False)
    historyOrders = user.hasorders.exclude(is_paid=False)
    total = 0

    for order in currentOrders:
        total += order.total
    total = float('%.2f' % total)
    context = {
        "user": user,
        "currentOrders": currentOrders,
        "historyOrders": historyOrders,
        "total": total
    }
    return render(request, "orders/cart.html", context)

def delete(request):
    txt = request.POST["option"]
    # return render(request, "orders/error.html", {"message": txt})
    order_id = []
    tmp = ""
    for t in txt:
        if t == '"':
            continue
        if t != " ":
            tmp +=t
        else:
            order_id.append(int(tmp))
            tmp = ""
    for id in order_id:
        try:
            order = Order.objects.get(pk=id)
        except Order.DoesNotExist:
            return render(request, "orders/error.html", {"message": "No order."})
        order.delete()
    return HttpResponseRedirect(reverse("cart"))

def checkout(request):
    user = request.user
    currentOrders = user.hasorders.filter(is_paid=False)
    total = 0

    for order in currentOrders:
        total += order.total
    total = total*100
    context = {
        "user": user,
        # "currentOrders": currentOrders,
        "total": total,
    }
    if (total == 0):
        return render(request,"orders/error.html", {"message":"You have nothing to pay."})
    return render(request, "orders/checkout.html", context)

def success(request):
    # Set your secret key. Remember to switch to your live secret key in production!
    # See your keys here: https://dashboard.stripe.com/account/apikeys
    stripe.api_key = 'sk_test_nlALYQACljoHpD0cJ1rrJX3l00ZsaeWphc'

    # Token is created using Stripe Checkout or Elements!
    # Get the payment token ID submitted by the form:
    # token = request.form['stripeToken'] # Using Flask

    # token=stripe.Token.create(
    #   card={
    #     "number": "4242424242424242",
    #     "exp_month": 4,
    #     "exp_year": 2021,
    #     "cvc": "314",
    #   },
    # )

    token = request.POST["stripeToken"]
    email = request.POST["stripeEmail"]

    user = request.user
    currentOrders = user.hasorders.filter(is_paid=False)
    total = 0

    for order in currentOrders:
        total += order.total
        order.is_paid = True
        order.status = 'M'
        order.save()

    total = total*100

    charge = stripe.Charge.create(
      amount=int(total),
      currency='usd',
      description='Example charge',
      source=token,
    )
    SendaEmail(toEmail=email,username=user.username)
    return render(request, "orders/success.html")

from django.urls import path

from . import views

urlpatterns = [
    path("<int:food_id>", views.food, name="food"),
    path("<int:food_id>/order", views.order, name="order"),
    path("cart", views.cart, name="cart"),
    path("ordertopping", views.ordertopping, name="ordertopping"),
    path("delete", views.delete, name="delete"),
    path("checkout", views.checkout, name="checkout"),
    path("success", views.success, name="success")
]

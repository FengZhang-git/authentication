from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("register", views.register_view, name="register"),
    path("logining", views.logining_view, name="logining"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout")
]

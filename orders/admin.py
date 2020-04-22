from django.contrib import admin

from .models import Food, Order, Type
# Register your models here.

admin.site.register(Food)
admin.site.register(Order)
admin.site.register(Type)
# admin.site.register(Cart)

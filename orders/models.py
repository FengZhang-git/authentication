from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Type(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return f" {self.name}"

class Food(models.Model):
    SIZES = (
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
    )
    name = models.CharField(max_length=64)
    size = models.CharField(max_length=1, choices=SIZES)
    price = models.FloatField()
    # number = models.IntegerField()
    type = models.ForeignKey(Type, on_delete=models.CASCADE, related_name="foods")

    def __str__(self):
        typename = Type.objects.get(pk=self.type.id)
        return f"{typename}-{self.name} ({self.get_size_display()}, {self.price}$) "

class Order(models.Model):
    STATUS = (
        ('O', 'Ordered'),
        ('M', 'Making'),
        ('D', 'Delivering'),
        ('C', 'Completed'),
    )
    user  = models.ForeignKey(User, on_delete=models.CASCADE, related_name="hasorders")
    food = models.ForeignKey(Food, on_delete=models.CASCADE, related_name="inorders")
    number = models.IntegerField()
    total = models.FloatField()
    status = models.CharField(max_length=1, choices=STATUS, default='O')
    is_paid = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if(self.is_paid):
            pay = "Paid"
        else:
            pay = "Unpaid"
        return f" {self.id}-{self.user.username} has ordered {self.number} {self.food}. Total fee:{self.total}$. {pay} Status:{self.get_status_display()}.Ordered Time:{self.date}"

    def is_valid_order(self):
        return (self.food.price * self.number) == self.total
# class Cart(models.Model):
#     username = models.ForeignKey(User, on_delete=models.CASCADE, related_name="hascart")
#     orders = models.ManyToManyField(Order, blank=True, related_name="incart")

from django.db.models import Max
from django.test import Client, TestCase

from .models import Type, Food, Order
from django.contrib.auth.models import User

# Create your tests here.
class ModelsTestCase(TestCase):

    def setUp(self):

        user = User.objects.create_user(username="feng", email="11@qq.com", password="1234")
        t1 = Type.objects.create(name="Regular Pizza")
        t2 = Type.objects.create(name="Sicilian Pizza")
        f1 = Food.objects.create(name="Cheese",size='S',price=12.7,type=t1)
        f2 = Food.objects.create(name="1 item", size='L',price=40.7,type=t2)
        o1 = Order.objects.create(user=user, food=f1, number=1, total=12.7, status='O')
        o2 = Order.objects.create(user=user, food=f2, number=2, total=40.7, status='M', is_paid=True)

    def test_foods_count(self):
        t = Type.objects.get(name="Regular Pizza")
        self.assertEqual(t.foods.count(), 1)

    def test_hasorders_count(self):
        user = User.objects.get(username="feng")
        self.assertEqual(user.hasorders.count(), 2)

    def test_inorders_count(self):
        f = Food.objects.get(name="Cheese")
        self.assertEqual(f.inorders.count(), 1)


    def test_valid_order(self):
        f = Food.objects.get(name="Cheese")
        user = User.objects.get(username="feng")
        o = Order.objects.get(user=user, food=f)
        self.assertTrue(o.is_valid_order())

    def test_invalid_order(self):
        f = Food.objects.get(name="1 item")
        user = User.objects.get(username="feng")
        o = Order.objects.get(user=user, food=f)
        self.assertFalse(o.is_valid_order())

    def test_index(self):
        c = Client()
        response = c.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["message"], None)

    def test_valid_food_page(self):
        f = Food.objects.get(name="Cheese")

        c = Client()
        response = c.get(f"/order/{f.id}")
        self.assertEqual(response.status_code, 200)

    def test_invalid_food_page(self):
        max_id = Food.objects.all().aggregate(Max("id"))["id__max"]

        c = Client()
        response = c.get(f"/order/{max_id + 1}")
        self.assertEqual(response.status_code, 404)

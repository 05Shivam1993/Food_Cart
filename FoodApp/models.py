from django.db import models
from django.conf import settings


class Order(models.Model):
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    name = models.CharField(max_length = 100)
    mobile = models.CharField(max_length = 15)
    email = models.EmailField()
    category = models.CharField(max_length = 6)
    dish_name = models.CharField(max_length = 50)
    quantity = models.IntegerField(default=1)
    delievery_status = models.BooleanField(default=False)
    cost = models.FloatField()
    address = models.CharField(max_length = 300)
    date = models.DateField(blank=True,null=True)
    cancel_order = models.BooleanField(default = False)

    def __str__(self):
        return self.dish_name


class Foods(models.Model):
    item = models.CharField(max_length = 25,null=False)
    price = models.FloatField(default = 0.0)
    category = models.CharField(max_length = 10)
    image= models.ImageField(blank=True)

    def __str__(self):
        return self.item

class Offers(models.Model):
    coupons = models.CharField(max_length = 20)
    percentage = models.CharField(max_length = 2, default = 0)
    cost_applicable = models.FloatField(default = 100.0)

    def __str__(self):
        return self.coupons

from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Programm(models.Model):
    name = models.CharField(max_length=10000, default=None)
    length = models.IntegerField()
    month_start = models.IntegerField()
    day_start = models.IntegerField()
    hour_start = models.IntegerField()
    minute_start = models.IntegerField()
    periodicity = models.IntegerField()
    capacity = models.IntegerField()
    price_adult = models.IntegerField()
    price_children = models.IntegerField()
    price_invalid = models.IntegerField()
    discount_price_adult = models.IntegerField()
    discount_price_invalid = models.IntegerField()
    discount_price_children = models.IntegerField()
    parent = models.IntegerField()

class Place(models.Model):
    name = models.CharField(max_length=10000, default=None)
    place = models.CharField(max_length=1000, default=None)
    image = models.FileField(upload_to="static/logo_place", null=True)
    description = models.CharField(max_length=1000000000000000, default=None)


class UserInfo(models.Model):
    user = models.ForeignKey(
        to=User, on_delete=models.CASCADE, default=1
    )
    gmail = models.CharField(max_length=100, default=None, null=True)
    telephone = models.CharField(max_length=100, default=None, null=True)


class Registr(models.Model):
    programm_id = models.ForeignKey(
        to=Programm, on_delete=models.CASCADE, default=1
    )
    user = models.ForeignKey(
        to=User, on_delete=models.CASCADE, default=1
    )
    adult_count = models.IntegerField()
    children_count = models.IntegerField()
    invalid_count = models.IntegerField()

class Favorite(models.Model):
    place = models.ForeignKey(
        to=Place, on_delete=models.CASCADE, default=1
    )
    user = models.ForeignKey(
        to=User, on_delete=models.CASCADE, default=1
    )
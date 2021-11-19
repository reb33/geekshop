from django.db import models

# Create your models here.


class Product(models.Model):
    name = models.CharField(max_length=100)
    img = models.CharField(max_length=100)
    cost = models.CharField(max_length=10)
    desc = models.CharField(max_length=100)

from django.db import models

# Create your models here.
from authapp.models import ShopUser
from products.models import Product


class Basket(models.Model):
    user = models.ForeignKey(ShopUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name='количество', default=0)
    create_timestamp = models.DateTimeField(auto_now_add=True)
    update_timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.username}|{self.product.name}'

    def sum(self):
        return self.quantity * self.product.price

    def total_sum(self):
        return sum(basket.sum() for basket in Basket.objects.filter(user=self.user))

    def total_quantity(self):
        return sum(basket.quantity for basket in Basket.objects.filter(user=self.user))

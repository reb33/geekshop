from django.db import models

# Create your models here.
from django.utils.functional import cached_property

from authapp.models import ShopUser
from products.models import Product


# class BasketQuerySet(models.QuerySet):
#
#     def delete(self, return_quantity=True):
#         if return_quantity:
#             for item in self:
#                 item.product.quantity += item.quantity
#                 item.product.save()
#         return super().delete()


class Basket(models.Model):
    # objects = BasketQuerySet.as_manager()

    user = models.ForeignKey(ShopUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name='количество', default=0)
    create_timestamp = models.DateTimeField(auto_now_add=True)
    update_timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.username}|{self.product.name}'

    def sum(self):
        return self.quantity * self.product.price

    @cached_property
    def get_user_baskets(self):
        return Basket.objects.filter(user=self.user)

    def total_sum(self):
        return sum(basket.sum() for basket in self.get_user_baskets)

    def total_quantity(self):
        return sum(basket.quantity for basket in self.get_user_baskets)

    @staticmethod
    def get_item_quantity(pk):
        return Basket.objects.get(pk=pk).quantity

    # def delete(self, return_quantity=True, *args, **kwargs):
    #     if return_quantity:
    #         self.product.quantity += self.quantity
    #         self.product.save()
    #     return super().delete(*args, **kwargs)
    #
    # def save(self, *args, **kwargs):
    #     if self.pk:
    #         self.product.quantity -= self.quantity - Basket.objects.get(pk=self.pk).quantity
    #     else:
    #         self.product.quantity -= self.quantity
    #     self.product.save()
    #     super().save(*args, **kwargs)



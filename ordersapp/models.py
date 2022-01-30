from django.db import models

# Create your models here.
from authapp.models import ShopUser
from products.models import Product


class Order(models.Model):
    FORMING = 'FM'
    SENT_TO_PROCEED = 'STP'
    PROCEEDED = 'PRD'
    PAID = 'PD'
    READY = 'RDY'
    CANCEL = 'CNC'

    ORDER_STATUS_CHOICES = (
        (FORMING, 'формируется'),
        (SENT_TO_PROCEED, 'отправлен в обработку'),
        (PAID, 'оплачен'),
        (PROCEEDED, 'обрабатывается'),
        (READY, 'готов к выдаче'),
        (CANCEL, 'отменен')
    )

    user = models.ForeignKey(to=ShopUser, on_delete=models.CASCADE)
    created = models.DateTimeField(verbose_name='создан', auto_now_add=True)
    updated = models.DateTimeField(verbose_name='обновлен', auto_now=True)
    status = models.CharField(verbose_name='статус', max_length=3, choices=ORDER_STATUS_CHOICES, default=FORMING)
    is_active = models.BooleanField(verbose_name='активен', default=True)

    class Meta:
        ordering = ('-created',)
        verbose_name = 'заказ'
        verbose_name_plural = 'заказы'

    def __str__(self):
        return 'Текущий заказ: {}'.format(self.id)

    # def get_total_quantity(self):
    #     return sum(map(lambda i: i.quantity, self.get_selected_related_items()))
    #
    # def get_total_cost(self):
    #     return sum(map(lambda i: i.get_product_cost(), self.get_selected_related_items()))

    def get_summary(self):
        return {
            'total_quantity': sum(map(lambda i: i.quantity, self.get_selected_related_items())),
            'total_cost': sum(map(lambda i: i.get_product_cost(), self.get_selected_related_items()))
        }

    def get_selected_related_items(self):
        if not getattr(self, '_selected_related_items', None):
            self._selected_related_items = self.orderitems.select_related()
        return self._selected_related_items

    def delete(self, *args, **kwargs):
        for item in self.orderitems.select_related():
            item.product.quantity += item.quantity
            item.product.save()

        self.is_active = False
        self.save()


class OrderItem(models.Model):
    order = models.ForeignKey(to=Order, related_name='orderitems', on_delete=models.CASCADE)
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name='количество', default=0)

    def get_product_cost(self):
        return self.quantity * self.product.price

    @staticmethod
    def get_item_quantity(pk):
        return OrderItem.objects.get(pk=pk).quantity

from datetime import timedelta
from pprint import pprint

from django.core.management import BaseCommand
from django.db import connection
from django.db.models import Q, F, When, Case, DecimalField, IntegerField
from prettytable import PrettyTable

from geekshop.utils import db_profile_by_type
from ordersapp.models import Order, OrderItem
from products.models import Product


class Command(BaseCommand):

    def handle(self, *args, **options):
        action_1 = 1
        action_2 = 2
        action_expired = 3

        action_1__time_delta = timedelta(hours=12)
        action_2__time_delta = timedelta(days=1)

        action_1__discount = 0.3
        action_2__discount = 0.15
        action_expired__discount = 0.05

        action_1__condition = Q(order__updated__lte=F('order__created')+action_1__time_delta)
        action_2__condition = Q(order__updated__gt=F('order__created') + action_1__time_delta) & \
                              Q(order__updated__lte=F('order__created') + action_2__time_delta)

        action_expired__condition = Q(order__updated__gt=F('order__created') + action_2__time_delta)

        action_1__order = When(action_1__condition, then=action_1)
        action_2__order = When(action_2__condition, then=action_2)
        action_expired__order = When(action_expired__condition, then=action_expired)

        action_1__price = When(action_1__condition,
                               then=F('product__price') * F('quantity') * action_1__discount)

        action_2__price = When(action_2__condition,
                               then=F('product__price') * F('quantity') * -action_2__discount)

        action_expired__price = When(action_expired__condition,
                                     then=F('product__price') * F('quantity') * action_expired__discount)

        test_orderss = OrderItem.objects.annotate(
            action_order=Case(
                action_1__order,
                action_2__order,
                action_expired__order,
                output_field=IntegerField(),
            )).annotate(
            total_price=Case(
                action_1__price,
                action_2__price,
                action_expired__price,
                output_field=DecimalField(),
            )).order_by('action_order', 'total_price').select_related()

        t = PrettyTable(['num', 'order', 'name', 'discount', 'time since purchase'])
        for orderitem in test_orderss:
            t.add_row([
                f'{orderitem.action_order:2}',
                f'заказ №{orderitem.pk:3}',
                f'{orderitem.product.name:15}',
                f'скидка {abs(orderitem.total_price):6.2f} руб.',
                f'{orderitem.order.updated - orderitem.order.created}'
            ])
        print(t)

    # def handle(self, *args, **options):
    #     test_products = Product.objects.filter(
    #         Q(category__name='Одежда') |
    #         Q(category__name='Обувь')
    #     ).select_related()
    #
    #     print(len(test_products))
    #     print(test_products)
    #
    #     db_profile_by_type('lern_db', '', connection.queries)



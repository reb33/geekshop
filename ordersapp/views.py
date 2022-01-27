# Create your views here.
from django.db import transaction
from django.db.models.signals import pre_save, pre_delete
from django.dispatch import receiver
from django.forms import inlineformset_factory
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

from baskets.models import Basket
from ordersapp.forms import OrderItemForm
from ordersapp.models import Order, OrderItem
from products.mixin import BaseClassContextMixin
from products.models import Product


class OrderList(ListView, BaseClassContextMixin):
    model = Order
    title = 'Geekshop - Список заказов'

    # template_name = 'ordersapp/order_list.html'

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


class OrderCreate(CreateView, BaseClassContextMixin):
    model = Order
    # form_class = OrderForm
    fields = []
    success_url = reverse_lazy('orders:list')
    title = 'Geekshop - Создание заказаа'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        OrderFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemForm, extra=0)
        if self.request.POST:
            formset = OrderFormSet(self.request.POST)
        else:
            basket_items = Basket.objects.filter(user=self.request.user).exclude(quantity=0).exclude(
                product__is_active=False).select_related()
            if basket_items:
                OrderFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemForm, extra=basket_items.count())
                formset = OrderFormSet()
                for form, basket in zip(formset.forms, basket_items):
                    form.initial['product'] = basket.product
                    form.initial['quantity'] = basket.quantity
                    form.initial['price'] = basket.product.price
            else:
                formset = OrderFormSet()
        context['orderitems'] = formset
        return context

    def form_valid(self, form):
        ctx = self.get_context_data()
        orderitems = ctx['orderitems']

        with transaction.atomic():
            form.instance.user = self.request.user
            self.object = form.save()
            if orderitems.is_valid():
                orderitems.instance = self.object
                orderitems.save()
            if self.object.get_total_cost() == 0:
                self.object.delete()

        return super().form_valid(form)

    def post(self, request, *args, **kwargs):
        basket_items = Basket.objects.filter(user=self.request.user).exclude(quantity=0)
        # basket_items.delete(return_quantity=False)
        basket_items.delete()
        return super().post(request, *args, **kwargs)


class OrderUpdate(UpdateView):
    model = Order
    fields = []
    success_url = reverse_lazy('orders:list')
    title = 'Geekshop - Редактирование заказаа'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        OrderFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemForm, extra=0)
        if self.request.POST:
            formset = OrderFormSet(self.request.POST, instance=self.object)
        else:
            queryset = self.object.orderitems.select_related()
            formset = OrderFormSet(instance=self.object, queryset=queryset)
            for form in formset:
                if form.instance.pk:
                    form.initial['price'] = form.instance.product.price
        context['orderitems'] = formset
        return context

    def form_valid(self, form):
        ctx = self.get_context_data()
        orderitems = ctx['orderitems']

        with transaction.atomic():
            if orderitems.is_valid():
                orderitems.instance = self.object
                orderitems.save()
            if self.object.get_total_cost() == 0:
                self.object.delete()

        return super().form_valid(form)


class OrderDelete(DeleteView, BaseClassContextMixin):
    model = Order
    success_url = reverse_lazy('orders:list')
    title = 'Geekshop - Удаление заказаа'


class OrderDetail(DetailView, BaseClassContextMixin):
    model = Order
    title = 'Geekshop - Просмотр заказа'


def order_forming_complete(request, pk):
    order = get_object_or_404(Order, pk=pk)
    order.status = Order.SENT_TO_PROCEED
    order.save()

    return HttpResponseRedirect(reverse('orders:list'))


def get_product_price(request, pk):
    return JsonResponse({'price': Product.objects.get(pk=pk).price})


@receiver(pre_save, sender=OrderItem)
@receiver(pre_save, sender=Basket)
def product_quantity_update_save(sender, instance, **kwargs):
    if instance.pk:
        instance.product.quantity -= instance.quantity - Basket.objects.get(pk=instance.pk).quantity
    else:
        instance.product.quantity -= instance.quantity
    instance.product.save()


@receiver(pre_delete, sender=OrderItem)
@receiver(pre_delete, sender=Basket)
def product_quantity_update_delete(sender, instance, **kwargs):
    instance.product.quantity += instance.quantity
    instance.product.save()

#     def delete(self, return_quantity=True, *args, **kwargs):
#         if return_quantity:
#             self.product.quantity += self.quantity
#             self.product.save()
#         return super().delete(*args, **kwargs)
#
#     def save(self, *args, **kwargs):
#         if self.pk:
#             self.product.quantity -= self.quantity - Basket.objects.get(pk=self.pk).quantity
#         else:
#             self.product.quantity -= self.quantity
#         self.product.save()
#         super().save(*args, **kwargs)

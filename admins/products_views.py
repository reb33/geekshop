from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from admins.forms import ProductForm
from products.models import Product


@user_passes_test(lambda u: u.is_superuser)
def admin_products(request):
    products = Product.objects.all()
    ctx = {
        'header': 'Продукты',
        'products': products
    }
    return render(request, 'admins/admin-products-read.html', ctx)


@user_passes_test(lambda u: u.is_superuser)
def admin_products_create(request):
    if request.method == 'POST':
        form = ProductForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('admins:admin_products'))
    else:
        form = ProductForm()
    ctx = {
        'header': 'Создать продукт',
        'form': form
    }
    return render(request, 'admins/admin-products-create.html', ctx)


@user_passes_test(lambda u: u.is_superuser)
def admin_products_update(request, product_id):
    product = Product.objects.get(id=product_id)
    if request.method == 'POST':
        form = ProductForm(instance=product, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Данные обновлены')
    else:
        form = ProductForm(instance=product)
    ctx = {
        'header': f'Редактирование товара | {product}',
        'product': product,
        'form': form
    }
    return render(request, 'admins/admin-products-update-delete.html', ctx)


@user_passes_test(lambda u: u.is_superuser)
def admin_products_delete(request, product_id):
    product = Product.objects.get(id=product_id)
    product.is_active = False
    product.save()
    messages.success(request, f'Продукт {product} отключен')
    return HttpResponseRedirect(reverse('admins:admin_products'))

from django.shortcuts import render

from admins.forms import ProductForm
from products.models import Product


def admin_products(request):
    products = Product.objects.all()
    ctx = {
        'header': 'Продукты',
        'products': products
    }
    return render(request, 'admins/admin-products-read.html', ctx)


def admin_products_create(request):
    if request.method == 'POST':
        form = ProductForm


def admin_products_update(request, product_id):
    pass


def admin_products_delete(request, product_id):
    pass

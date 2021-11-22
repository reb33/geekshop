from django.shortcuts import render

from products.models import Product, ProductCategory


def main(request):
    ctx = {
        'title': 'GeekShop'
    }
    return render(request, 'index.html', ctx)


def products(request):
    items = Product.objects.all()
    categories = ProductCategory.objects.all()
    ctx = {
        'title': 'GeekShop - Каталог',
        'products': items,
        'categories': categories
    }
    print()
    return render(request, 'products.html', ctx)

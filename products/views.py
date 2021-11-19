from django.shortcuts import render


# Create your views here.
from products.models import Product


def main(request):
    ctx = {
        'title': 'GeekShop'
    }
    return render(request, 'index.html', ctx)


def products(request):
    items = Product.objects.all()
    ctx = {
        'title': 'GeekShop - Каталог',
        'products': items
    }
    print()
    return render(request, 'products.html', ctx)

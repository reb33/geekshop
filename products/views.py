from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render

from products.models import Product, ProductCategory


def main(request):
    ctx = {
        'title': 'GeekShop'
    }
    return render(request, 'index.html', ctx)


def products(request, id_category=None, page=1):
    categories = ProductCategory.objects.all()

    if id_category:
        items = Product.objects.filter(category=id_category)
    else:
        items = Product.objects.all()
    paginator = Paginator(items, per_page=3)
    try:
        products_paginator = paginator.page(page)
    except PageNotAnInteger:
        products_paginator = paginator.page(1)
    except EmptyPage:
        products_paginator = paginator.page(paginator.num_pages)

    ctx = {
        'title': 'GeekShop - Каталог',
        'products': products_paginator,
        'categories': categories
    }
    return render(request, 'products.html', ctx)

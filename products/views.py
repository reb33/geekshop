from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string

from products.models import Product, ProductCategory


def main(request):
    ctx = {
        'title': 'GeekShop'
    }
    return render(request, 'index.html', ctx)


def products(request):
    categories = ProductCategory.objects.all()
    id_category = request.GET.get('id_category')
    page = request.GET.get('page', 1)

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
    if request.is_ajax():
        result = render_to_string('includes/card.html', ctx)
        return JsonResponse({'result': result})
    return render(request, 'products.html', ctx)

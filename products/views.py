from django.conf import settings
from django.core.cache import cache
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.views.generic import DetailView

from products.models import Product, ProductCategory


def main(request):
    ctx = {
        'title': 'GeekShop'
    }
    return render(request, 'index.html', ctx)


def get_link_categories():
    if settings.LOW_CACHE:
        key = 'links_categories'
        categories = cache.get(key)
        if categories is None:
            categories = ProductCategory.objects.filter(is_active=True)
            cache.set(key, categories)
        return categories
    else:
        return ProductCategory.objects.filter(is_active=True)


def get_link_products():
    if settings.LOW_CACHE:
        key = 'links_products'
        _products = cache.get(key)
        if _products is None:
            _products = Product.objects.filter(is_active=True).select_related('category')
            cache.set(key, _products)
        return _products
    else:
        return Product.objects.filter(is_active=True).select_related('category')


def get_link_product(pk):
    if settings.LOW_CACHE:
        key = f'links_product_{pk}'
        product = cache.get(key)
        if product is None:
            product = Product.objects.get(pk)
            cache.set(key, product)
        return product
    else:
        return Product.objects.get(pk)


def products(request):
    # categories = ProductCategory.objects.all()
    products = get_link_products()
    categories = get_link_categories()
    id_category = request.GET.get('id_category')
    page = request.GET.get('page', 1)

    if id_category:
        items = [p for p in products if int(p.category_id) == int(id_category)]
        # items = Product.objects.filter(category=id_category).select_related('category')
    else:
        items = products
        # items = Product.objects.all().select_related('category')
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


class ProductDetails(DetailView):
    template_name = 'detail.html'
    model = Product

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        product = get_link_product(kwargs.get('pk'))
        ctx['product'] = product
        return ctx



from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from admins.forms import CategoryForm
from products.models import ProductCategory


def admin_categories(request):
    cats = ProductCategory.objects.all()
    ctx = {
        'header': 'Категории',
        'categories': cats
    }
    return render(request, 'admins/admin-categories-read.html', ctx)


def admin_categories_create(request):
    if request.method == 'POST':
        form = CategoryForm(data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('admins:admin_categories'))
    else:
        form = CategoryForm()
    ctx = {
        'header': 'Создать категорию',
        'form': form
    }
    return render(request, 'admins/admin-categories-create.html', ctx)


def admin_categories_update(request, cat_id):
    cat = ProductCategory.objects.get(id=cat_id)
    if request.method == 'POST':
        form = CategoryForm(instance=cat, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Данные обновлены')
    else:
        form = CategoryForm(instance=cat)
    ctx = {
        'header': f'Редактирование категории товаров | {cat.name}',
        'category': cat,
        'form': form
    }
    return render(request, 'admins/admin-categories-update-delete.html', ctx)


def admin_categories_delete(request, cat_id):
    cat = ProductCategory.objects.get(id=cat_id)
    cat.is_active = False
    cat.save()
    messages.success(request, f'Категория продуктов {cat.name} отключена')
    return HttpResponseRedirect(reverse('admins:admin_categories'))

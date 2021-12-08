from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from admins.forms import AdminUserRegistrationForm, AdminUserEditForm
from authapp.models import ShopUser


@user_passes_test(lambda u: u.is_superuser)
def admin_users(request):
    users = ShopUser.objects.all()
    ctx = {
        'header': 'Пользователи',
        'users': users
    }
    return render(request, 'admins/admin-users-read.html', ctx)


@user_passes_test(lambda u: u.is_superuser)
def admin_users_create(request):
    if request.method == 'POST':
        form = AdminUserRegistrationForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('admins:admin_users'))
    ctx = {
        'header': 'Создание пользователя',
        'form': AdminUserRegistrationForm()
    }
    return render(request, 'admins/admin-users-create.html', ctx)


@user_passes_test(lambda u: u.is_superuser)
def admin_users_update(request, user_id):
    user = ShopUser.objects.get(id=user_id)
    if request.method == 'POST':
        form = AdminUserEditForm(instance=user, data=request.POST, files=request.FILES)
        if form.is_valid():
            messages.success(request, 'Данные обновлены')
            form.save()
            user = ShopUser.objects.get(id=user_id)
        else:
            print(form.errors)
    else:
        form = AdminUserEditForm(instance=user)
    ctx = {
        'header': f'Редактирование пользователя | {user.username}',
        'selected_user': user,
        'form': form
    }
    return render(request, 'admins/admin-users-update-delete.html', ctx)


@user_passes_test(lambda u: u.is_superuser)
def admin_users_delete(request, user_id):
    user = ShopUser.objects.get(id=user_id)
    user.is_active = False
    user.save()
    messages.success(request, f'Пользователь {user.username} отключен')
    return HttpResponseRedirect(reverse('admins:admin_users'))
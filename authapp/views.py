from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from authapp.forms import ShopUserLoginForm, ShopUserRegistrationForm, UserProfileForm
from baskets.models import Basket


def login(request):
    if request.method == 'POST':
        login_form = ShopUserLoginForm(data=request.POST)
        if login_form.is_valid():
            username = login_form.data['username']
            password = login_form.data['password']
            user = auth.authenticate(username=username, password=password)
            if user.is_active:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('main'))
    else:
        login_form = ShopUserLoginForm()
    ctx = {
        'title': 'GeekShop - Авторизация',
        'form': login_form
    }
    return render(request, 'authapp/login.html', ctx)


def register(request):
    if request.method == 'POST':
        form = ShopUserRegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Вы успешно зарегистрировались')
            return HttpResponseRedirect(reverse('authapp:login'))
    else:
        form = ShopUserRegistrationForm()
    ctx = {
        'title': 'GeekShop - Регистрация',
        'form': form
    }
    return render(request, 'authapp/register.html', ctx)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('main'))


@login_required
def profile(request):
    if request.method == 'POST':
        form = UserProfileForm(instance=request.user, data=request.POST, files=request.FILES)
        if form.is_valid():
            messages.success(request, 'Данные обновлены')
            form.save()
        else:
            print(form.errors)
    else:
        form = UserProfileForm(instance=request.user)
    ctx = {
        'title': 'GeekShop - Профиль',
        'form': form,
        'baskets': Basket.objects.filter(user=request.user)
    }
    return render(request, 'authapp/profile.html', ctx)

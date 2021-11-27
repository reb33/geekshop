from django.contrib import auth
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from authapp.forms import ShopUserLoginForm, ShopUserRegistrationForm


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

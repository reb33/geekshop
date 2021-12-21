import contextlib

from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView, LoginView
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import FormView, UpdateView

from authapp.forms import ShopUserLoginForm, ShopUserRegistrationForm, UserProfileForm, UserProfileEditForm
from authapp.models import ShopUser
from baskets.models import Basket
from geekshop.settings import EMAIL_HOST_USER, DOMAIN_NAME
from products.mixin import BaseClassContextMixin, UserDispatchMixin


class LoginListView(LoginView, BaseClassContextMixin):
    template_name = "authapp/login.html"
    form_class = ShopUserLoginForm
    title = "GeekShop - Login"
    success_url = reverse_lazy('main')

# def login(request):
#     if request.method == "POST":
#         login_form = ShopUserLoginForm(data=request.POST)
#         if login_form.is_valid():
#             username = login_form.data["username"]
#             password = login_form.data["password"]
#             user = auth.authenticate(username=username, password=password)
#             if user.is_active:
#                 auth.login(request, user)
#                 return HttpResponseRedirect(reverse("main"))
#     else:
#         login_form = ShopUserLoginForm()
#     ctx = {"title": "GeekShop - Авторизация", "form": login_form}
#     return render(request, "authapp/login.html", ctx)


class RegisterListView(FormView, BaseClassContextMixin):
    model = ShopUser
    template_name = "authapp/register.html"
    form_class = ShopUserRegistrationForm
    title = "GeekShop - Регистрация"
    success_url = reverse_lazy("authapp:login")

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST)
        if form.is_valid():
            user = ''
            try:
                user = form.save()
                if self.send_verify_link(user):
                    messages.success(request, "Вы успешно зарегистрировались")
                    return HttpResponseRedirect(self.get_success_url())
                else:
                    messages.error(request, "Не удалось отправить сообщение")
                    user.delete()
            except Exception as e:
                with contextlib.suppress(Exception):
                    user.delete()
                raise e
        return render(request, self.template_name, {"form": form})

    def send_verify_link(self, user):
        activation_link = reverse("authapp:verify", args=[user.email, user.activation_key])
        subject = f"Активизация пользователя {user.username} на портале Geekshop"
        message = f"Для активации пользователя передийте по ссылке \n{DOMAIN_NAME}{activation_link}"
        return send_mail(
            subject, message, EMAIL_HOST_USER, [user.email], fail_silently=True
        )

    @staticmethod
    def verify(request, email, activation_key):
        try:
            user = ShopUser.objects.get(email=email)
            if (
                user
                and user.activation_key == activation_key
                and not user.is_activation_key_expires()
                and not user.is_active
            ):
                user.activation_key = ''
                user.activation_key_expires = None
                user.is_active = True
                user.save()
                auth.login(request, user)
            return render(request, 'authapp/verification.html')
        except Exception as e:
            print(e)
            return HttpResponseRedirect(reverse("main"))


class Logout(LogoutView):
    template_name = 'index.html'

# def logout(request):
#     auth.logout(request)
#     return HttpResponseRedirect(reverse("main"))


class ProfileUpdateView(UpdateView, BaseClassContextMixin, UserDispatchMixin):
    model = ShopUser
    template_name = "authapp/profile.html"
    form_class = UserProfileForm
    title = "GeekShop - Профиль"
    success_url = reverse_lazy("authapp:profile")

    def post(self, request, *args, **kwargs):
        form = UserProfileForm(data=request.POST, files=request.FILES, instance=request.user)
        profile_form = UserProfileEditForm(data=request.POST, instance=request.user.userprofile)
        if form.is_valid() and profile_form.is_valid():
            form.save()
        return redirect(self.success_url)

    def form_valid(self, form):
        messages.success(self.request, 'Данные обновлены')
        return super().form_valid(form)

    def get_object(self, queryset=None):
        return get_object_or_404(self.model, pk=self.request.user.pk)

    # baskets передаеься через контекстный процессор products.context_processors.basket
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['profile'] = UserProfileEditForm(instance=self.request.user.userprofile)
        return ctx



# @login_required
# def profile(request):
#     if request.method == "POST":
#         form = UserProfileForm(
#             instance=request.user, data=request.POST, files=request.FILES
#         )
#         if form.is_valid():
#             messages.success(request, "Данные обновлены")
#             form.save()
#         else:
#             print(form.errors)
#     else:
#         form = UserProfileForm(instance=request.user)
#     ctx = {
#         "title": "GeekShop - Профиль",
#         "form": form,
#         "baskets": Basket.objects.filter(user=request.user),
#     }
#     return render(request, "authapp/profile.html", ctx)

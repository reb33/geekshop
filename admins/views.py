from django.contrib.auth.decorators import user_passes_test
from django.db.models import F
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from admins.forms import AdminUserRegistrationForm, AdminUserEditForm
from admins.forms import CategoryForm
from admins.forms import ProductForm
from authapp.models import ShopUser
from products.mixin import BaseClassContextMixin, SuperUserDispatchMixin
from products.models import Product
from products.models import ProductCategory


# Create your views here.


@user_passes_test(lambda u: u.is_superuser)
def index(request):
    ctx = {"header": "Административная панель"}
    return render(request, "admins/base.html", ctx)


class CategoryListView(ListView, SuperUserDispatchMixin, BaseClassContextMixin):
    model = ProductCategory
    template_name = "admins/admin-categories-read.html"
    title = "Список категорий"


class CategoryCreateView(CreateView, SuperUserDispatchMixin, BaseClassContextMixin):
    model = ProductCategory
    template_name = "admins/admin-categories-create.html"
    form_class = CategoryForm
    success_url = reverse_lazy("admins:admin_categories")
    title = "Создать категорию"


class CategoryUpdateView(UpdateView, SuperUserDispatchMixin, BaseClassContextMixin):
    model = ProductCategory
    template_name = "admins/admin-categories-update-delete.html"
    form_class = CategoryForm
    success_url = reverse_lazy("admins:admin_categories")
    title = "Редактировать категорию"

    def form_valid(self, form):
        if form.cleaned_data.get('is_active'):
            self.get_object().product_set.update(is_active=True)
        if 'discount' in form.changed_data:
            prev_discount = form.initial['discount']
            discount = form.cleaned_data['discount']
            if discount != 0 or prev_discount != 0:
                print(f'скидка {discount}% для категории {self.object.name}')
                if prev_discount != 0:
                    self.object.product_set.update(price=F('price') / (prev_discount / 100) * (1 - discount / 100))
                else:
                    self.object.product_set.update(price=F('price') * (1 - discount / 100))
        return super().form_valid(form)


class CategoryDeleteView(DeleteView, SuperUserDispatchMixin, BaseClassContextMixin):
    model = ProductCategory
    template_name = "admins/admin-categories-update-delete.html"
    success_url = reverse_lazy("admins:admin_categories")
    title = "Удалить категорию"

    def delete(self, request, *args, **kwargs):
        self.object: ProductCategory = self.get_object()
        self.object.is_active = False
        self.object.save()
        self.object.product_set.update(is_active=False)
        return HttpResponseRedirect(self.get_success_url())


class ProductListView(ListView, SuperUserDispatchMixin, BaseClassContextMixin):
    model = Product
    template_name = "admins/admin-products-read.html"
    title = "Список продуктов"

    def get_queryset(self):
        return Product.objects.all().select_related()


class ProductCreateView(CreateView, SuperUserDispatchMixin, BaseClassContextMixin):
    model = Product
    form_class = ProductForm
    template_name = "admins/admin-products-create.html"
    success_url = reverse_lazy("admins:admin_products")
    title = "Создать продукт"


class ProductUpdateView(UpdateView, SuperUserDispatchMixin, BaseClassContextMixin):
    model = Product
    form_class = ProductForm
    template_name = "admins/admin-products-update-delete.html"
    success_url = reverse_lazy("admins:admin_products")
    title = "Редактировать продукт"


class ProductDeleteView(DeleteView, SuperUserDispatchMixin, BaseClassContextMixin):
    model = Product
    template_name = "admins/admin-products-update-delete.html"
    success_url = reverse_lazy("admins:admin_products")
    title = "Редактировать продукт"

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class UserListView(ListView, SuperUserDispatchMixin, BaseClassContextMixin):
    model = ShopUser
    template_name = "admins/admin-users-read.html"
    title = "Список пользователей"


class UserCreateView(CreateView, SuperUserDispatchMixin, BaseClassContextMixin):
    model = ShopUser
    template_name = "admins/admin-users-create.html"
    form_class = AdminUserRegistrationForm
    success_url = reverse_lazy("admins:admin_users")
    title = "Создание пользователя"


class UserUpdateView(UpdateView, SuperUserDispatchMixin, BaseClassContextMixin):
    model = ShopUser
    template_name = "admins/admin-users-update-delete.html"
    form_class = AdminUserEditForm
    success_url = reverse_lazy("admins:admin_users")
    title = "Редактирование пользователя"


class UserDeleteView(DeleteView, SuperUserDispatchMixin, BaseClassContextMixin):
    model = ShopUser
    template_name = "admins/admin-users-update-delete.html"
    form_class = AdminUserEditForm
    success_url = reverse_lazy("admins:admin_users")
    title = "Удалить пользователя"

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()
        success_url = self.get_success_url()
        return HttpResponseRedirect(success_url)

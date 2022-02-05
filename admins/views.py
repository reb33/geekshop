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
from products.mixin import UserDispatchMixin, BaseClassContextMixin
from products.models import Product
from products.models import ProductCategory


# Create your views here.


@user_passes_test(lambda u: u.is_superuser)
def index(request):
    ctx = {"header": "Административная панель"}
    return render(request, "admins/base.html", ctx)


class CategoryListView(ListView, UserDispatchMixin, BaseClassContextMixin):
    model = ProductCategory
    template_name = "admins/admin-categories-read.html"
    title = "Список категорий"


class CategoryCreateView(CreateView):
    model = ProductCategory
    template_name = "admins/admin-categories-create.html"
    form_class = CategoryForm
    success_url = reverse_lazy("admins:admin_categories")
    title = "Создать категорию"


class CategoryUpdateView(UpdateView):
    model = ProductCategory
    template_name = "admins/admin-categories-update-delete.html"
    form_class = CategoryForm
    success_url = reverse_lazy("admins:admin_categories")
    title = "Редактировать категорию"

    def form_valid(self, form):
        if form.cleaned_data.get('is_active'):
            self.get_object().product_set.update(is_active=True)
        if 'discount' in form.cleaned_data:
            discount = form.cleaned_data['discount']
            if discount:
                print(f'скидка {discount}% для категории {self.object.name}')
                self.object.product_set.update(price=F('price') * (1 - discount / 100))
        return super().form_valid(form)


class CategoryDeleteView(DeleteView):
    model = ProductCategory
    template_name = "admins/admin-categories-update-delete.html"
    success_url = reverse_lazy("admins:admin_categories")
    title = "Удалить категорию"

    def delete(self, request, *args, **kwargs):
        obj: ProductCategory = self.get_object()
        obj.is_active = False
        obj.save()
        obj.product_set.update(is_active=False)
        return HttpResponseRedirect(self.get_success_url())


class ProductListView(ListView, UserDispatchMixin, BaseClassContextMixin):
    model = Product
    template_name = "admins/admin-products-read.html"
    title = "Список продуктов"

    def get_queryset(self):
        return Product.objects.all().select_related()


class ProductCreateView(CreateView, UserDispatchMixin, BaseClassContextMixin):
    model = Product
    form_class = ProductForm
    template_name = "admins/admin-products-create.html"
    success_url = reverse_lazy("admins:admin_products")
    title = "Создать продукт"


class ProductUpdateView(UpdateView, UserDispatchMixin, BaseClassContextMixin):
    model = Product
    form_class = ProductForm
    template_name = "admins/admin-products-update-delete.html"
    success_url = reverse_lazy("admins:admin_products")
    title = "Редактировать продукт"


class ProductDeleteView(DeleteView, UserDispatchMixin, BaseClassContextMixin):
    model = Product
    template_name = "admins/admin-products-update-delete.html"
    success_url = reverse_lazy("admins:admin_products")
    title = "Редактировать продукт"

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.is_active = False
        obj.save()
        return HttpResponseRedirect(self.get_success_url())


class UserListView(ListView, UserDispatchMixin, BaseClassContextMixin):
    model = ShopUser
    template_name = "admins/admin-users-read.html"
    title = "Список пользователей"


class UserCreateView(CreateView, UserDispatchMixin, BaseClassContextMixin):
    model = ShopUser
    template_name = "admins/admin-users-create.html"
    form_class = AdminUserRegistrationForm
    success_url = reverse_lazy("admins:admin_users")
    title = "Создание пользователя"


class UserUpdateView(UpdateView, UserDispatchMixin, BaseClassContextMixin):
    model = ShopUser
    template_name = "admins/admin-users-update-delete.html"
    form_class = AdminUserEditForm
    success_url = reverse_lazy("admins:admin_users")
    title = "Редактирование пользователя"


class UserDeleteView(DeleteView, UserDispatchMixin, BaseClassContextMixin):
    model = ShopUser
    template_name = "admins/admin-users-update-delete.html"
    form_class = AdminUserEditForm
    success_url = reverse_lazy("admins:admin_users")
    title = "Удалить пользователя"

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.is_active = False
        obj.save()
        return HttpResponseRedirect(self.get_success_url())

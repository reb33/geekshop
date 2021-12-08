from django.urls import path

from admins.views import (
    index
)
from admins.categories_views import admin_categories, admin_categories_create, admin_categories_update, \
    admin_categories_delete
from admins.users_views import admin_users, admin_users_create, admin_users_update, admin_users_delete
from admins.products_views import admin_products, admin_products_create, admin_products_update, admin_products_delete

app_name = 'admins'

urlpatterns = [
    path('', index, name='index'),
    path('users', admin_users, name='admin_users'),
    path('categories', admin_categories, name='admin_categories'),
    path('products', admin_products, name='admin_products'),

    path('users-create', admin_users_create, name='admin_users_create'),
    path('categories-create', admin_categories_create, name='admin_categories_create'),
    path('products-create', admin_products_create, name='admin_products_create'),

    path('users-update/<int:user_id>', admin_users_update, name='admin_users_update'),
    path('categories-update/<int:cat_id>', admin_categories_update, name='admin_categories_update'),
    path('products-update/<int:product_id>', admin_products_update, name='admin_products_update'),

    path('users-delete/<int:user_id>', admin_users_delete, name='admin_users_delete'),
    path('categories-delete/<int:cat_id>', admin_categories_delete, name='admin_categories_delete'),
    path('product-delete/<int:product_id>', admin_products_delete, name='admin_products_delete'),

]

from django.urls import path, re_path

from products.views import products

app_name = 'products'

urlpatterns = [
    path('', products, name='main')
]

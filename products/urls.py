from django.urls import path

from products.views import products

app_name = 'products'

urlpatterns = [
    path('', products, name='main'),
    path('category/<int:id_category>', products, name='category'),
    path('page/<int:page>', products, name='page')
]

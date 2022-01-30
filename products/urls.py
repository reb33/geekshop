from django.urls import path

from products.views import products, ProductDetails

app_name = 'products'

urlpatterns = [
    path('', products, name='main'),
    path('detail/<int:pk>/', ProductDetails.as_view(), name='detail'),
]

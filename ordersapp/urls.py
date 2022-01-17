from django.urls import path, re_path

from ordersapp.views import (
    OrderList, OrderCreate, OrderUpdate, OrderDetail, OrderDelete, order_forming_complete, get_product_price
)

app_name = 'orders'

urlpatterns = [
    path(r'', OrderList.as_view(), name='list'),
    path(r'create', OrderCreate.as_view(), name='create'),
    path(r'update/<int:pk>', OrderUpdate.as_view(), name='update'),
    path(r'read/<int:pk>', OrderDetail.as_view(), name='read'),
    path(r'delete/<int:pk>', OrderDelete.as_view(), name='delete'),
    re_path(r'^forming/complete/(?P<pk>\d+)/$',
            order_forming_complete, name='forming_complete'),

    path(r'get_product_price/<int:pk>', get_product_price, name='get_product_price')
]

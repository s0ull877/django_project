
from django.urls import path

from orders.views import OrderCreateViews, OrderSuccess, OrderListView

app_name = 'orders'

urlpatterns = [
    path('order_create/', OrderCreateViews.as_view(), name='order_create'),
    path('order_success/', OrderSuccess.as_view(), name='succeeded'),
    path('', OrderListView.as_view(), name='orders_list'),
]

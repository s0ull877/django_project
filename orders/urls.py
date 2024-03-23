
from django.urls import path

from orders.views import OrderCreateViews

app_name = 'orders'

urlpatterns = [
    path('order_create/', OrderCreateViews.as_view(), name='order_create'),

]


from django.views.generic.edit import CreateView 

from common.views import TitleMixin

from orders.forms import OrderForm

class OrderCreateViews(TitleMixin, CreateView):

    template_name = 'orders\order-create.html'
    title = 'Store - Оформление заказа'
    form_class = OrderForm
import uuid

from yookassa import Payment

from django.conf import settings
from django.urls import reverse_lazy
from django.shortcuts import HttpResponseRedirect,reverse
from django.views.generic.edit import CreateView 
from django.views.generic.base import TemplateView 
from products.context_processors import baskets

from common.views import TitleMixin

from orders.forms import OrderForm                                                              

class OrderSuccess(TitleMixin,TemplateView):
    template_name = "orders\success.html"
    title = 'Store - Спасибо за заказ'


class OrderCreateViews(TitleMixin, CreateView):

    template_name = 'orders\order-create.html'
    title = 'Store - Оформление заказа'
    form_class = OrderForm
    success_url = reverse_lazy('orders:order_create')
    
    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)

        user_basket = baskets(request)

        payment = Payment.create({
            "amount": {
                "value": user_basket['baskets'].total_sum(),
                "currency": "RUB"
            },
            "confirmation": {
                "type": "redirect",
                "return_url": "{}{}".format(settings.DOMAIN_NAME, reverse('orders:succeeded'))
            },
            "capture": True,
            "description": "Заказ в Store",
            'metadata': {
                'testkey': 'testvalue'
            }
        }, uuid.uuid4())

        return HttpResponseRedirect(payment.confirmation.confirmation_url)

    def form_valid(self, form):
        form.instance.initiator = self.request.user
        return super().form_valid(form)
    
import json
import uuid

from yookassa import Payment

from django.conf import settings
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.views.generic.edit import CreateView 
from django.views.generic.base import TemplateView
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import HttpResponseRedirect,reverse

from products.context_processors import baskets

from orders.models import Order


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
            "description": f"Заказ в Store #{self.object.id}",
            'metadata': {
                'order_id': self.object.id
            }
        }, uuid.uuid4())

        return HttpResponseRedirect(payment.confirmation.confirmation_url)

    def form_valid(self, form):

        form.instance.initiator = self.request.user
        return super().form_valid(form)
    


@csrf_exempt
def yookassa_webhook_view(request):
    
    payload = request.body.decode('utf-8')
    payload_dict = json.loads(payload)
    # status = payload_dict['object']['status']

    order_id = int(payload_dict['object']['metadata']['order_id'])

    try:
        
        order = Order.objects.get(id=order_id)

        if not order.status:
            order.update_after_payment()

    except Order.DoesNotExist:
        pass



    return HttpResponse(status=200)
# coding: utf-8


from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.contenttypes.models import ContentType

from .base import OrderBaseView, OrderParamsValidatorMixin


class AccountList(OrderBaseView, OrderParamsValidatorMixin):

    """ Order List View. Receives get params
        and response neither arguments in get
        request params.

        GET Params:

        1. AJAX - if ajax is True, we have response
        html part, that insert in DOM structure in client
        side. If we have True, we response all html
        document with base template.

        ALL PARAMS put in params_storage after validate
    """

    request_params_slots = {
        'ajax': [None, 0],
    }

    session_params_slots = {
    }

    def __init__(self, *args, **kwargs):
        self.params_storage = {}
        self.output_context = {
            'cart': None,
        }
        super(OrderList, self).__init__(*args, **kwargs)

    def get(self, *args, **kwargs):
        self._aggregate()

        if not self.params_storage['ajax']:
            return render_to_response(
                'blocks/order/order_list_general.html',
                self.output_context,
                context_instance=RequestContext(self.request), )
        else:
            return render_to_response(
                'blocks/order/order_list_ajax.html',
                self.output_context,
                context_instance=RequestContext(self.request), )

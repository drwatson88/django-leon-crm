# coding: utf-8

import django_filters
from django.forms import ModelForm

from .models import Order, OrderItem, ShippingMethod
from person.models import Org, OrgType
from staff.models import Staff


class OrderForm(ModelForm):

    class Meta:
        model = Order
        fields = ['org_client', 'org_provider', 'client_staff',
                  'comment', 'order_status', 'shipping_method',
                  'pay_method', 'order_date', 'delivery_time',
                  'manager_order', 'manager_sale', 'designer']


# class OrderItemForm(ModelForm):
#
#     class Meta:
#         model = OrderItem
#         fields = ('first_name', 'last_name', 'middle_name',
#                   'role', 'phone', 'email')


# org_type_client = OrgType.objects.filter(name='client').all()[0]
# org_type_provider = OrgType.objects.filter(name='provider').all()[0]


class OrderListFilter(django_filters.FilterSet):

    order_date__gte = django_filters.DateFilter(label='Дата заказа с',
                                                lookup_expr='gte',
                                                name='order_date',
                                                help_text='Дата заказа с')
    order_date__lte = django_filters.DateFilter(label='Дата заказа по',
                                                lookup_expr='lte',
                                                name='order_date',
                                                help_text='Дата заказа по')
    org_client = django_filters.ModelChoiceFilter(label='Клиент',
                                                  queryset=Org.objects.
                                                  filter(org_type='client').all(),
                                                  help_text='Выберите организацию клиента')
    org_provider = django_filters.ModelChoiceFilter(label='Поставщик',
                                                    queryset=Org.objects.
                                                    filter(org_type='provider').all(),
                                                    help_text='Выберите организацию поставщика')
    manager_order = django_filters.ModelChoiceFilter(label='Менеджер заказа',
                                                     queryset=Staff.objects.all(),
                                                     help_text='Выберите менеджера заказа')
    delivery_time = django_filters.DateFilter(label='Срок поставки',
                                              help_text='Выберите организацию поставщика')
    shipping_method = django_filters.ModelChoiceFilter(label='Способ доставки',
                                                       queryset=ShippingMethod.objects.all(),
                                                       help_text='Выберите cпособ доставки')

    class Meta:
        model = Order
        fields = ['order_date', 'org_client', 'org_provider',
                  'manager_order', 'delivery_time', 'shipping_method']

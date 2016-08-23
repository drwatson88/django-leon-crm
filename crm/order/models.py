# coding: utf-8

from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from person.models import OrgEmployee
from staff.models import Staff
from person.models import Org
# from catalog.models import PrintType


class OrderStatus(models.Model):

    name = models.CharField(verbose_name='Статус заказа', max_length=255,
                            primary_key=True)
    official = models.CharField(verbose_name='Наименование статуса заказа',
                                max_length=255)


class ShippingMethod(models.Model):

    name = models.CharField(verbose_name='Способ доставки', max_length=255,
                            primary_key=True)
    official = models.CharField(verbose_name='Наименование способа доставки',
                                max_length=255)


class PayMethod(models.Model):

    name = models.CharField(verbose_name='Способ оплаты', max_length=255,
                            primary_key=True)
    official = models.CharField(verbose_name='Наименование способа оплаты',
                                max_length=255)


class Order(models.Model):

    org_client = models.ForeignKey(Org, related_name='org_client',
                                   verbose_name='Наименование организации покупателя')
    org_provider = models.ForeignKey(Org, related_name='org_provider',
                                     verbose_name='Наименование организации продавца')
    client_staff = models.ForeignKey(OrgEmployee, verbose_name='Сотрудник клиента')
    comment = models.CharField(verbose_name='Комментарии', max_length=255)
    order_status = models.ForeignKey(OrderStatus, verbose_name='Статус заказа')
    shipping_method = models.ForeignKey(ShippingMethod, related_name='shipping_method',
                                        verbose_name='Статус доставки')
    pay_method = models.ForeignKey(ShippingMethod, related_name='pay_method',
                                   verbose_name='Способ оплаты')
    order_date = models.DateTimeField(verbose_name='Дата заказа')
    delivery_time = models.DateTimeField(verbose_name='Срок поставки')
    manager_order = models.ForeignKey(Staff, related_name='manager_order',
                                      verbose_name='Менеджер заказа')
    manager_sale = models.ForeignKey(Staff, related_name='manager_sale',
                                     verbose_name='Менеджер продаж')
    designer = models.ForeignKey(Staff, related_name='designer', verbose_name='Дизайнер')


class OrderItem(models.Model):

    pass

    # order = models.ForeignKey(Order, verbose_name='Заказ')
    # quantity = models.PositiveIntegerField(verbose_name='Количество')
    # print_type = models.ForeignKey(PrintType, verbose_name='Вид нанесения')
    # unit_price = models.IntegerField(verbose_name='Цена (ед.)')
    # item_price = models.IntegerField(verbose_name='Цена за компект')
    #
    # product_content_type = models.ForeignKey(ContentType)
    # product_object_id = models.PositiveIntegerField()
    # product_content_object = GenericForeignKey('product_content_type', 'product_object_id')
    #
    # class Meta:
    #     verbose_name = u'order item'
    #     verbose_name_plural = u'order items'
    #     ordering = (u'order',)
    #
    # def get_product(self):
    #     return self.product_content_object
    #
    # def set_product(self, product):
    #     self.product_content_object = product
    #
    # product = property(get_product, set_product)
    #
    # def get_type(self):
    #     return self.product_content_type

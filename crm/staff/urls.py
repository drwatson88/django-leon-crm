# coding: utf-8

from django.conf.urls import patterns, url
from .views import OrderList

urlpatterns = patterns('account.views',
                       url(r'^add_item', CartList.as_view(), name='add'),
                       url(r'^update_item', CartList.as_view(), name='update'),
                       url(r'^remove_item', CartList.as_view(), name='remove'),
                       # url(r'^context_list', ''),
                       url(r'^list', CartList.as_view(), name='list'))

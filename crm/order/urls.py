# coding: utf-8

from django.conf.urls import patterns, url
from .views import OrderCreate


urlpatterns = patterns('order.views',
                       url(r'^order_create', OrderCreate.as_view(), name='order_create'),
                       # url(r'^org_detail/(?P<pk>.*)/$', OrgDetail.as_view(), name='org_detail'),
                       # url(r'^org_list', OrgList.as_view(), name='org_list'),
                       #
                       # url(r'^employee_create/(?P<org_pk>.*)/$', EmployeeCreate.as_view(),
                       #     name='employee_create'),
                       )
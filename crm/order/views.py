# coding: utf-8


from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404, Http404
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.views.generic.list import ListView
from django.core.urlresolvers import reverse, reverse_lazy
from django.db import models

from .models import Order #, OrderItem
from .forms import OrderListFilter


class OrderCreate(CreateView):

    extra_context = {"extra_title": u"Добавить заказ"}
    model = Order
    template_name = 'crm/blocks/order/order_create.html'
    fields = ['org_client', 'org_owner', 'client_staff',
              'comment', 'order_status', 'shipping_method',
              'pay_method', 'order_date', 'delivery_time',
              'manager_order', 'manager_sale', 'designer']
    context_object_name = 'form'

    def get_success_url(self):
        return reverse("order_detail", kwargs={"pk": self.object.pk})

    def get_context_data(self, **kwargs):
        context = super(OrderCreate, self).get_context_data(**kwargs)
        for k, v in self.extra_context.items():
            context.update({k: v})
        return context


class OrderUpdate(UpdateView):

    extra_context = {"title": u"Редактирование"}
    model = Order
    template_name = 'crm/blocks/order/order_create.html'
    fields = ['org_client', 'org_owner', 'client_staff',
              'comment', 'order_status', 'shipping_method',
              'pay_method', 'order_date', 'delivery_time',
              'manager_order', 'manager_sale', 'designer']
    context_object_name = 'form'

    def get_success_url(self):
        return reverse("order_detail", kwargs={"pk": self.object.pk})

    def get_context_data(self, **kwargs):
        context = super(OrderUpdate, self).get_context_data(**kwargs)
        for k, v in self.extra_context.items():
            context.update({k: v})
        return context


class OrderDelete(DeleteView):

    extra_context = {"title": u"Удалить"}
    model = Order
    template_name = 'crm/blocks/order/tmp.html'
    context_object_name = 'order_list'
    success_url = reverse_lazy('list')


class OrderDetail(CreateView):

    extra_context = {'extra_title': 'Просмотреть заказ'}
    model = Order
    template_name = 'crm/blocks/order/order_detail.html'
    fields = ['org_client', 'org_owner', 'client_staff',
              'comment', 'order_status', 'shipping_method',
              'pay_method', 'order_date', 'delivery_time',
              'manager_order', 'manager_sale', 'designer']
    context_object_name = 'order'

    def get_context_data(self, **kwargs):
        context = super(OrderDetail, self).get_context_data(**kwargs)

        form = OrderDetail(instance=self.object)
        for field in form.fields:
            form.fields[field].widget.attrs['disabled'] = True

        context.update({'form': form,
                        'order_item_list': self.get_object(self.queryset).
                        orderitem_set.all()})
        for k, v in self.extra_context.items():
            context.update({k: v})
        return context


class OrderList(ListView):

    extra_context = {'extra_title': 'Поиск организации'}
    queryset = Order.objects.all()
    filter_cls = OrderListFilter
    template_name = 'crm/blocks/order/order_list.html'
    context_object_name = 'order_list'
    paginate_by = 30

    def __init__(self, **kwargs):
        super(OrderList, self).__init__(**kwargs)
        self.filter = None

    def get_context_data(self, **kwargs):
        context = super(OrderList, self).get_context_data(**kwargs)
        context['filter'] = self.filter_cls(self.request.GET, queryset=self.queryset)
        for k, v in self.extra_context.items():
            context.update({k: v})
        return context


# class OrderItemCreate(FormView):
#     extra_context = {"title": u"Добавить товар"}
#     form_class = OrderItem
#     context_object_name = "form"
#     template_name = "crm/blocks/order/xxx.html"
#
#     def __init__(self, **kwargs):
#         super(OrderItemCreate, self).__init__(**kwargs)
#         self.order_pk = None
#         self.order = None
#
#     def dispatch(self, request, *args, **kwargs):
#         if "pk" in kwargs:
#             try:
#                 self.order_pk = int(kwargs['order_pk'])
#             except ValueError:
#                 raise Http404()
#
#             try:
#                 self.order = Order.objects.get(pk=self.order_pk)
#             except models.ObjectDoesNotExist:
#                 raise Http404()
#         return super(OrderItemCreate, self).dispatch(request, *args, **kwargs)
#
#     def get_success_url(self):
#         return reverse("order_detail", kwargs={"pk": self.order_pk})
#
#     def form_valid(self, form):
#         cd = form.cleaned_data
#
#         order_item = OrderItem(first_name=cd['first_name'], last_name=cd['last_name'],
#                                middle_name=cd['middle_name'], phone=cd['phone'],
#                                email=cd['email'], org=self.order_pk)
#         order_item.save()
#         return super(OrderItemCreate, self).form_valid(form)
#
#
# class OrderItemEdit(FormView):
#
#     extra_context = {"title": u"Редактировать товар"}
#     form_class = OrderItemForm
#     context_object_name = "form"
#     template_name = "crm/blocks/person/xxx.html"
#
#     def __init__(self, **kwargs):
#         super(OrderItemEdit, self).__init__(**kwargs)
#         self.pk = None
#         self.order_item = None
#
#     def dispatch(self, request, *args, **kwargs):
#         if "pk" in kwargs:
#             try:
#                 self.pk = int(kwargs["pk"])
#             except ValueError:
#                 raise Http404()
#
#             try:
#                 self.order_item = OrderItem.objects.get(pk=self.pk)
#             except models.ObjectDoesNotExist:
#                 raise Http404()
#
#         else:
#             raise Http404()
#
#         return super(OrderItemEdit, self).dispatch(request, *args, **kwargs)
#
#     def get_success_url(self):
#         return reverse("order_detail", kwargs={"pk": self.order_item.order.pk})
#
#     def form_valid(self, form):
#         cd = form.cleaned_data
#
#         self.order_item.save()
#         return super(OrderItemEdit, self).form_valid(form)

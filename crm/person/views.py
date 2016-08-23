# coding: utf-8


from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404, \
    Http404, HttpResponseRedirect
from django.views.generic.edit import CreateView, UpdateView, \
    DeleteView, FormView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.core.urlresolvers import reverse, reverse_lazy
from django.db import models

from .models import Org, OrgEmployee
from .forms import OrgForm, OrgListFilter, EmployeeForm


class OrgCreate(CreateView):

    extra_context = {"extra_title": u"Добавить организацию"}
    model = Org
    template_name = 'crm/blocks/person/org_create.html'
    fields = ['title', 'inn', 'kpp', 'ogrn', 'legal_address',
              'actual_address', 'org_type', 'bank', 'checking_account',
              'phone', 'email']
    context_object_name = 'form'

    def get_success_url(self):
        return reverse("org_detail", kwargs={"pk": self.object.pk})

    def get_context_data(self, **kwargs):
        context = super(OrgCreate, self).get_context_data(**kwargs)
        for k, v in self.extra_context.items():
            context.update({k: v})
        return context


class OrgUpdate(UpdateView):

    extra_context = {"title": u"Редактирование"}
    model = Org
    template_name = 'crm/blocks/person/tmp.html'
    fields = ['title', 'inn', 'kpp', 'ogrn', 'legal_address',
              'actual_address', 'org_type', 'bank', 'checking_account',
              'phone', 'email']
    context_object_name = 'org'

    def get_success_url(self):
        return reverse("org_detail", kwargs={"pk": self.object.pk})


class OrgDelete(DeleteView):

    extra_context = {"title": u"Удалить"}
    model = Org
    template_name = 'crm/blocks/person/tmp.html'
    context_object_name = 'org_list'
    success_url = reverse_lazy('list')


class OrgDetail(DetailView):

    extra_context = {'extra_title': 'Просмотреть организацию'}
    model = Org
    template_name = 'crm/blocks/person/org_detail.html'
    fields = ['title', 'inn', 'kpp', 'ogrn', 'legal_address',
              'actual_address', 'org_type', 'bank',
              'checking_account', 'phone', 'email']
    context_object_name = 'org'

    def get_context_data(self, **kwargs):
        context = super(OrgDetail, self).get_context_data(**kwargs)

        form = OrgForm(instance=self.object)
        for field in form.fields:
            form.fields[field].widget.attrs['disabled'] = True

        context.update({'form': form,
                        'org_employee_list': self.get_object(self.queryset).
                        orgemployee_set.all()})
        for k, v in self.extra_context.items():
            context.update({k: v})
        return context


class OrgList(ListView):

    extra_context = {'extra_title': 'Поиск организации'}
    queryset = Org.objects.all()
    filter_cls = OrgListFilter
    template_name = 'crm/blocks/person/org_list.html'
    context_object_name = 'org_list'
    paginate_by = 30

    def __init__(self, **kwargs):
        super(OrgList, self).__init__(**kwargs)
        self.filter = None

    def get_context_data(self, **kwargs):
        context = super(OrgList, self).get_context_data(**kwargs)
        context['filter'] = self.filter_cls(self.request.GET, queryset=self.queryset)
        for k, v in self.extra_context.items():
            context.update({k: v})
        return context


class EmployeeCreate(CreateView):

    extra_context = {'extra_title': u"Добавить к организации сотрудника"}
    form_class = EmployeeForm
    template_name = 'crm/blocks/person/org_employee_create.html'
    context_object_name = 'form'

    def __init__(self, **kwargs):
        super(EmployeeCreate, self).__init__(**kwargs)
        self.org_pk = None
        self.org = None

    def dispatch(self, request, *args, **kwargs):
        if 'org_pk' in kwargs:
            try:
                self.org_pk = int(kwargs['org_pk'])
            except ValueError:
                raise Http404()

            try:
                self.org = Org.objects.get(pk=self.org_pk)
            except models.ObjectDoesNotExist:
                raise Http404()
        return super(EmployeeCreate, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse("org_detail", kwargs={"pk": self.org_pk})

    def get_context_data(self, **kwargs):
        context = super(EmployeeCreate, self).get_context_data(**kwargs)
        for k, v in self.extra_context.items():
            context.update({k: v})
        return context

    def form_valid(self, form):
        cd = form.cleaned_data

        employee = OrgEmployee(first_name=cd['first_name'], last_name=cd['last_name'],
                               middle_name=cd['middle_name'], phone=cd['phone'],
                               email=cd['email'], org=self.org)
        employee.save()
        return HttpResponseRedirect(self.get_success_url())


class EmployeeEdit(FormView):

    extra_context = {"title": u"Редактировать товар"}
    form_class = EmployeeForm
    context_object_name = "form"
    template_name = 'crm/blocks/person/org_employee_create.html'

    def __init__(self, **kwargs):
        super(EmployeeEdit, self).__init__(**kwargs)
        self.pk = None
        self.employee = None

    def dispatch(self, request, *args, **kwargs):
        if "pk" in kwargs:
            try:
                self.pk = int(kwargs["pk"])
            except ValueError:
                raise Http404()

            try:
                self.employee = OrgEmployee.objects.get(pk=self.pk)
            except models.ObjectDoesNotExist:
                raise Http404()

        else:
            raise Http404()

        return super(EmployeeEdit, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse("org_detail", kwargs={"pk": self.employee.org.pk})

    def form_valid(self, form):
        cd = form.cleaned_data

        self.employee.first_name = cd['first_name']
        self.employee.last_name = cd['last_name']
        self.employee.middle_name = cd['middle_name']
        self.employee.phone = cd['phone']
        self.employee.email = cd['email']
        self.employee.save()
        return super(EmployeeEdit, self).form_valid(form)

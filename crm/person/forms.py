# coding: utf-8

import django_filters
from django.forms import ModelForm, Form

from .models import Org, OrgType, OrgEmployee


class OrgForm(ModelForm):

    class Meta:
        model = Org
        fields = ['title', 'inn', 'kpp', 'ogrn', 'legal_address',
                  'actual_address', 'org_type', 'bank',
                  'checking_account', 'phone', 'email']


class EmployeeForm(ModelForm):

    class Meta:
        model = OrgEmployee
        fields = ('first_name', 'last_name', 'middle_name',
                  'role', 'phone', 'email')


class OrgListFilter(django_filters.FilterSet):

    title__name = django_filters.CharFilter(label='Наименование организации',
                                            lookup_expr='icontains',
                                            name='title',
                                            help_text='Строка должна содержать '
                                                      'полное имя организации или часть')
    inn__name = django_filters.CharFilter(label='ИНН организации',
                                          lookup_expr='icontains',
                                          name='inn',
                                          help_text='Строка должна содержать '
                                                    'полное ИНН организации или часть')
    org_type = django_filters.ModelChoiceFilter(label='Тип организации',
                                                queryset=OrgType.objects.all(),
                                                help_text='Выберите тип организации')

    class Meta:
        model = Org
        fields = ['org_type']

# coding: utf-8


import json
import itertools
from .list_extra import ListExtraConverter, list_unit_extra

from django.db.models import Q
from django.core.paginator import Paginator

from leon.base import BaseView, BaseParamsValidatorMixin


class UnitListParamsValidationMixin(BaseParamsValidatorMixin):
    """ Mixin with validators for validate
        request parameters.
    """

    @staticmethod
    def _filter_validator(value, default):
        return value if value else default

    @staticmethod
    def _page_no_validator(value, default):
        return value if value else default

    @staticmethod
    def _page_start_validator(value, default):
        return value if value else default

    @staticmethod
    def _page_stop_validator(value, default):
        return value if value else default

    @staticmethod
    def _page_size_validator(value, default):
        return value if value else default


class UnitListView(BaseView, ListExtraConverter, UnitListParamsValidationMixin):
    """
    Class for Unit List View
    (use in parent factory class)
    """

    kwargs_params_slots = {
    }

    request_params_slots = {
        'filter': [None, '[]'],
        'page_no': [None, 1],
        'page_size': [None, 10],
        'page_start': [None, 1],
        'page_stop': [None, 10]
    }

    template_name = None
    per_page_count = None

    MODEL = None
    FIELDS = []

    filter_form_class = None
    redirect_url = None
    list_develop_extra = None
    list_unit_extra = list_unit_extra

    PAGE_STEP = None

    def __init__(self, **kwargs):
        """
        :param kwargs:
        """
        self.params_storage = {}
        self.output_context = {
            'filter': None,
            'table': None,
            'page_s': None
        }
        super(UnitListView, self).__init__(**kwargs)
        self.table = {}
        self.extra = {}

    def _filter_header(self):
        pass

    def _create_filter(self):
        self.filter_data = json.loads(self.params_storage['filter'])
        self.filter = {
            'filter': self.filter_form_class(self.filter_data) if self.filter_data
            else self.filter_form_class(),
            'header': self.list_unit_extra['filter']['header']
        }

    def _format_filter(self):
        self.filter = self.FILTER_FORMAT_WIDGET().format(self.filter['filter'],
                                                         self.filter['header'],
                                                         'filter_form',
                                                         self.extra['filter']['groups'],
                                                         self.extra['filter']['buttons'],
                                                         self.extra['subtype'],
                                                         None)

    def _format_page_list(self):
        self.page_start = (self.page_no // self.PAGE_STEP) * self.PAGE_STEP + 1
        self.page_stop = min((self.page_no // self.PAGE_STEP + 1) * self.PAGE_STEP, self.page_count)
        self.page_s = [
            {
                'id': k,
                'active': (True if k == self.page_no else False)
            } for k in range(self.page_start, self.page_stop + 1)]

    def _create_qs_list(self):
        query = self.MODEL.objects

        q_chain = [Q(**{'{}__icontains'.format(field): value})
                   for field, value in (self.filter_data or {}) if value]
        q = q_chain.pop() if q_chain else None
        for item in q_chain:
            q &= item

        query = query.filter(q) if q else query
        self.qs = query.all()
        pages = Paginator(self.qs, self.per_page_count)
        self.page = pages.page(self.params_storage['page_no'])
        self.object_list = self.page.object_list

    def _get_model_verbose_name(self, field):
        return self.MODEL._meta._forward_fields_map[field]._verbose_name

    def _format_qs_list_header(self):
        self.table['header_s'] = [self._get_model_verbose_name(field) for field in self.FIELDS]

    def _format_qs_list(self):
        object_list = self.object_list
        self.table['row_s'] = []
        for obj in object_list:
            row = []
            for field in self.FIELDS:
                row.append(getattr(obj, field))
            self.table['row_s'].append(row)

    def _create_page_list(self):

        in_page_no = self.params_storage['page_no']
        in_page_size = self.params_storage['page_size']
        in_page_start = self.params_storage['page_start']
        in_page_stop = self.params_storage['page_stop']

        product_obj_s_count = len(self.qs)

        self.page_count = product_obj_s_count//in_page_size + \
                          (product_obj_s_count % in_page_size > 0)

        if in_page_no == 'next':
            self.page_no = int(in_page_stop) + 1
        elif in_page_no == 'prev':
            self.page_no = int(in_page_start) - 1
        else:
            self.page_no = int(in_page_no)

        if self.page_count < self.page_no or 0 >= self.page_no:
            self.page_no = 1

    def get(self, *args, **kwargs):
        self._create_filter()
        self._create_qs_list()
        self._create_page_list()

        self._convert_extra()

        self._format_filter()
        self._format_page_list()
        self._format_qs_list_header()
        self._format_qs_list()
        self._aggregate()
        return self._render()

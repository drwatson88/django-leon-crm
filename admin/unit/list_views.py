# coding: utf-8


import json
import pymorphy2

from django.db.models import Q
from django.core.paginator import Paginator

from leon.base import BaseView, BaseParamsValidatorMixin
from admin.unit.base_forms import UnitFilterWidgetMixin


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


class UnitListView(BaseView, UnitListParamsValidationMixin):
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

    HEADER = None
    MODEL = None
    FIELDS = []

    filter_main_class = None
    filter_mixin_class = UnitFilterWidgetMixin
    redirect_url = None

    PAGE_STEP = None

    first_table_col_header = '<i class="fa fa-pencil-square-o" aria-hidden="true"></i>'
    last_table_col_header = '<i class="fa fa-times" aria-hidden="true"></i>'

    first_table_col_pattern = \
        '<a style="color: gray" href="{href}"><i class="fa fa-pencil-square-o" ' \
        'aria-hidden="true"></i></a>'
    last_table_col_pattern = \
        '<a style="color: gray" href="{href}"><i class="fa fa-times" ' \
        'aria-hidden="true"></i></a>'

    first_item_link_pattern = ''
    last_item_link_pattern = ''

    buttons_pack = None

    meta = None

    def __init__(self, **kwargs):
        """
        :param kwargs:
        """
        self.params_storage = {}
        self.output_context = {
            'filter': None,
            'table': None,
            'page_s': None,
            'unit_buttons_pack': None
        }
        super(UnitListView, self).__init__(**kwargs)
        self.table = {}
        self.extra = {}

    def _create_buttons_pack(self):
        self.unit_buttons_pack = self.buttons_pack

    def _create_filter_class(self):
        self.filter_class = type('FilterClass',
                                 tuple([self.filter_main_class,
                                        self.filter_mixin_class]),
                                 {})

    def _create_filter(self):
        self.filter_data = json.loads(self.params_storage['filter'])
        self.filter = self.filter_class(self.filter_data) \
            if self.filter_data else self.filter_class()

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

    def _get_model_field_verbose_name(self, field):
        return self.MODEL._meta._forward_fields_map[field]._verbose_name

    def _get_model_verbose_name(self):
        return self.MODEL._meta.verbose_name

    def _format_qs_list_header(self):
        morph = pymorphy2.MorphAnalyzer()
        morph_obj = morph.parse(self._get_model_verbose_name().lower())[0]
        self.table['header'] = self.HEADER.format(morph_obj.inflect({'plur',
                                                                     'gent'}).word)

    def _format_qs_list(self):
        self.table['header_s'] = [self.first_table_col_header] + \
                                 [self._get_model_field_verbose_name(field)
                                  for field in self.FIELDS] + \
                                 [self.last_table_col_header]

        object_list = self.object_list
        self.table['row_s'] = []
        for obj in object_list:
            row = [self.first_table_col_pattern.format(
                href=self.first_item_link_pattern.format(getattr(obj, 'id')))]
            for field in self.FIELDS:
                row.append(getattr(obj, field))
            row.append(self.last_table_col_pattern.format(
                href=self.last_item_link_pattern.format(getattr(obj, 'id'))))
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

        self.page_start = (self.page_no // self.PAGE_STEP) * self.PAGE_STEP + 1
        self.page_stop = min((self.page_no // self.PAGE_STEP + 1) * self.PAGE_STEP, self.page_count)
        self.page_s = [
            {
                'id': k,
                'active': (True if k == self.page_no else False)
            } for k in range(self.page_start, self.page_stop + 1)
        ]

    def _create_meta(self):
        self.unit_meta = json.dumps(self.meta)

    def get(self, *args, **kwargs):
        self._create_filter_class()
        self._create_filter()
        self._create_buttons_pack()
        self._create_qs_list()
        self._create_page_list()
        self._create_meta()

        self._format_qs_list_header()
        self._format_qs_list()

        self._aggregate()
        return self._render()

# coding: utf-8


import json
from digg_paginator import DiggPaginator
from leon.base import BaseView, BaseParamsValidatorMixin


PAGE_SIZE = 20


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

    """ Unit List View. Receives get params
        and response neither arguments in get
        request params.

        GET Params:

        1. AJAX - if ajax is True, we have response
        html part, that insert in DOM structure in client
        side. If we have True, we response all html
        document with base template.
        2. GRID - grid or list
        3. GRID_CNT - count columns in grid
        4. ORDER - sort order
        5. PAGE_NO - page number
        6. PAGE_SIZE - size of page (count = rows*columns)

        ALL PARAMS put in params_storage after validate
    """

    UNIT_MODEL = None
    FILTER_MODEL = None

    page_size = PAGE_SIZE
    context_processors = []

    kwargs_params_slots = {
    }

    request_params_slots = {
        'page': [None, 1],
    }

    def __init__(self, *args, **kwargs):
        self.params_storage = {}
        self.output_context = {
            'page': None,
        }
        super(UnitListView, self).__init__(*args, **kwargs)

    def _unit_query(self):
        self.unit_set = self.UNIT_MODEL.objects.all()

    def _filter_s(self):
        """

        :return:
        """

        self.filter_set = self.FILTER_MODEL.all().order_by('position')
        self.filter_set = self.filter_set.order_by('position')

        for filter_obj in self.filter_set:
            if filter_obj.type in ['M2M', 'FK']:
                json_value = json.loads(filter_obj.value)
                filter_value = self.params_storage.get(filter_obj.name) or \
                               (json_value['filter'] and self.params_storage[json_value['filter']])

                if filter_value:
                    self.product_set = self.product_set.\
                        filter(**{'{abbr}__value'.format(abbr=filter_obj.name): filter_value})

            if filter_obj.type == 'KV':
                json_value = json.loads(filter_obj.value)
                filter_value = self.params_storage.get(filter_obj.name) or \
                               (json_value['filter'] and self.params_storage[json_value['filter']])

                if filter_value:
                    product_id_s = self.product_set.values_list('id', flat=True)
                    product_kv_id_s = self.CATALOG_PRODUCT_PARAMS_KV_MODEL.objects. \
                        filter(**{'{rel}__in'.format(rel=json_value['related_query']): product_id_s}). \
                        filter(abbr=filter_obj.name).\
                        filter(value=filter_value).\
                        values('{rel}__pk'.format(rel=json_value['related_query']), flat=True)
                    self.product_set = self.product_set.filter(pk__in=product_kv_id_s)

    def _set_order_s(self):
        order = self.params_storage['order']
        self.order_s = self.ORDER_REFERENCE_MODEL.objects.order_by('-position').all()
        for order_obj in self.order_s:
            order_obj.selected = False
            if order_obj.name == order:
                order_obj.selected = True
        order_selected = self.ORDER_REFERENCE_MODEL.objects.get(name=order)
        self.order_name = order_selected.field_name \
            if order_selected.field_order else '-{}'.format(order_selected.field_name)

    def _unit_obj_s_query(self):
        self.unit_obj_s_query = self.UNIT_MODEL.objects.all()

    def _unit_s_query(self):
        paginator = DiggPaginator(self.product_obj_s_query, self.page_size)
        self.page = paginator.page(self.params_storage['page'] or 1)

    def get(self, *args, **kwargs):
        self._unit_query()
        self._filter_s()
        self._set_order_s()
        self._unit_obj_s_query()
        self._product_s_query()
        self._aggregate()
        return self._render()

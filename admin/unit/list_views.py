# coding: utf-8


import json
import itertools
from django.db.models import Q
from django.core.paginator import Paginator

from leon.base import BaseView, BaseParamsValidatorMixin


class UnitMasterParamsValidationMixin(BaseParamsValidatorMixin):
    """ Mixin with validators for validate
        request parameters.
    """

    @staticmethod
    def _pk_validator(value, default):
        try:
            return int(value)
        except BaseException as exc:
            return default

    @staticmethod
    def _csrftoken_validator(value, default):
        return value

    @staticmethod
    def _data_validator(value, default):
        return value


class UnitMasterListView(BaseView):
    """
    Class for Unit Create View
    (use in parent factory class)
    """

    kwargs_params_slots = {
    }

    request_params_slots = {
        'filter': [None, '[]'],
        'page': [None, 1]
    }

    template_name = None
    per_page_count = None

    MODEL = None

    filter_form_class = None
    redirect_url = None
    develop_extra = None
    unit_extra = None

    def __init__(self, **kwargs):
        """
        :param kwargs:
        """
        self.params_storage = {}
        self.output_context = {
            'filter': None,
            'table': None,
            'pages': None
        }
        super(UnitMasterListView, self).__init__(**kwargs)

    def _filter_header(self):
        pass

    def _create_filter(self):
        self.filter = json.loads(self.params_storage['filter'])

    def _format_filter(self):
        pass

    def _qs_list_header(self):
        pass

    def _create_qs_list(self):
        query = self.MODEL.objects

        q_chain = [Q(**{'{}__icontains'.format(field): value})
                   for field, value in (self.filter or {}) if value]
        q = q_chain.pop()
        for item in q_chain:
            q &= item

        pages = Paginator(query.filter(q).all(), self.per_page_count)
        self.page = pages.page(self.params_storage['page'])

    def get(self, *args, **kwargs):
        self._aggregate()
        return self._render()
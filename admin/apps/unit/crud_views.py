# coding: utf-8


import json
import pymorphy2
import itertools
from django.shortcuts import HttpResponseRedirect, HttpResponse

from leon.base import BaseView, BaseParamsValidatorMixin


class UnitParamsValidationMixin(BaseParamsValidatorMixin):
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

    @staticmethod
    def _unit_validator(value, default):
        return value


class UnitCRUDView(BaseView):
    """
    Class for Unit CRUD View
    (use in parent factory class)
    """

    kwargs_params_slots = {
    }

    request_params_slots = {
        'data': [None, []]
    }

    template_name = None
    model = None
    redirect_url = None
    meta = None
    breadcrumb_page = None

    def __init__(self, **kwargs):
        """

        :param kwargs:
        """
        self.params_storage = {}
        self.output_context = {
            'unit_master_form': None
        }
        super(UnitCRUDView, self).__init__(**kwargs)
        self.extra = {}

    def _redirect(self):
        return HttpResponse(json.dumps({'url': self.redirect_url}))

    def _render_content(self):
        response = self._render()
        html = response.content
        return HttpResponse(json.dumps({'url': None,
                                        'html': html.decode('utf-8')}))

    def _validate_master_form(self):
        if self.unit_master_form.is_valid():
            self.unit_master_form.save()
            return True


class UnitCreateView(UnitCRUDView):
    """
    Class for Unit Create View
    (use in parent factory class)
    """

    def get(self, *args, **kwargs):
        self._create_master_form()
        self._create_slave_form_s()
        self._create_meta()
        self._create_breadcrumb()

        self._format()

        self._aggregate()
        return self._render()

    def post(self, *args, **kwargs):
        self._create_master_form(get=False)
        if self._validate_master_form():
            return self._redirect()
        self._create_slave_form_s()
        self._create_meta()
        self._create_breadcrumb()

        self._format()

        self._aggregate()
        return self._render_content()


class UnitUpdateView(UnitCRUDView):
    """
    Class for Unit Update View
    (use in parent factory class)

    relation_qs_s = [
        {
            'header_s': [],
            'queryset': None,
        }
    ]
    """

    kwargs_params_slots = {
        'unit': [None, 1]
    }

    first_table_col_header = '<i class="fa fa-pencil-square-o" aria-hidden="true"></i>'
    last_table_col_header = '<i class="fa fa-times" aria-hidden="true"></i>'

    def _create_master_form(self, get=True):
        instance_s = self.model.objects.filter(id=int(self.params_storage['unit'])).all()
        self.unit_master_form = self.master_form_class(instance=instance_s[0]) \
            if instance_s else self.master_form_class()
        self.unit_master_form.is_valid()

    def _get_row_s(self, queryset, field_s):
        row_s = []
        for obj in queryset:
            row = [self.first_table_col_pattern.format(
                href=self.first_item_link_pattern.format(getattr(obj, 'id')))]
            for field in field_s:
                row.append(getattr(obj, field))
            row.append(self.last_table_col_pattern.format(
                href=self.last_item_link_pattern.format(getattr(obj, 'id'))))
            row_s.append(row)

    def _create_relation_tables(self):
        self.relation_tables = [
            {
                'header_s': [self.first_table_col_header] +
                            [self._get_model_field_verbose_name(field)
                             for field in t['header_s']] +
                            [self.last_table_col_header],
                'row_s': self._get_row_s(getattr(self, t['queryset'])(), t['header_s'])
            } for t in self.relation_qs_s
        ]

    def _get_model_field_verbose_name(self, field):
        return self.model._meta._forward_fields_map[field]._verbose_name

    def _get_model_verbose_name(self):
        return self.model._meta.verbose_name

    def get(self, *args, **kwargs):
        self._create_master_form()
        self._create_slave_form_s()
        self._create_meta()
        self._create_breadcrumb()

        self._format()

        self._aggregate()
        return self._render()

    def post(self, *args, **kwargs):
        self._create_master_form(get=False)
        if self._validate_master_form():
            return self._redirect()
        self._create_slave_form_s()
        self._create_meta()
        self._create_breadcrumb()

        self._format()

        self._aggregate()
        return self._render_content()

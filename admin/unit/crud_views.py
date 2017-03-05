# coding: utf-8


import json
import pymorphy2
import itertools
from django.shortcuts import HttpResponseRedirect, HttpResponse

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


class UnitMasterCRUDView(BaseView):
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
    master_form_class = None
    slave_form_class_s = None
    redirect_url = None
    meta = None

    def __init__(self, **kwargs):
        """

        :param kwargs:
        """
        self.params_storage = {}
        self.output_context = {
            'unit_master_form': None,
            'unit_slave_form_s': None,
            'unit_meta': None
        }
        super(UnitMasterCRUDView, self).__init__(**kwargs)
        self.extra = {}

    def _create_master_form(self, get=True):
        self.unit_master_form = self.master_form_class() if get \
            else self.master_form_class(json.loads(self.params_storage['data']))

    def _create_slave_form_s(self):
        self.unit_slave_form_s = [slave_form_class()
                                  for slave_form_class in self.slave_form_class_s]

    def _create_meta(self):
        self.unit_meta = json.dumps(self.meta)

    def _create_breadcrumb(self):
        pass

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


class UnitMasterCreateView(UnitMasterCRUDView):
    """
    Class for Unit Create View
    (use in parent factory class)
    """

    def get(self, *args, **kwargs):
        self._create_breadcrumb()
        self._create_master_form()
        self._create_slave_form_s()
        self._create_meta()

        self._aggregate()
        return self._render()

    def post(self, *args, **kwargs):
        self._create_breadcrumb()
        self._create_master_form(get=False)
        if self._validate_master_form():
            return self._redirect()
        self._create_slave_form_s()
        self._create_meta()
        self._aggregate()
        return self._render_content()


class UnitMasterUpdateView(UnitMasterCRUDView):
    """
    Class for Unit Update View
    (use in parent factory class)
    """

    def get(self, *args, **kwargs):
        self._create_breadcrumb()
        self._create_master_form()
        self._create_slave_form_s()
        self._create_meta()

        self._aggregate()
        return self._render()

    def post(self, *args, **kwargs):
        self._create_breadcrumb()
        self._create_master_form(get=False)
        if self._validate_master_form():
            return self._redirect()
        self._create_slave_form_s()
        self._create_meta()
        self._aggregate()
        return self._render_content()

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
    }

    unit_form_class = None
    template_name = None
    UNIT_MODEL = None

    def __init__(self, **kwargs):
        """

        :param kwargs:
        """
        self.params_storage = {}
        self.output_context = {
            'unit_form': None
        }
        super(UnitCRUDView, self).__init__(**kwargs)

    def _create_form(self):
        self.unit_form = self.unit_form_class(initial=self.params_storage)

    def _validate_form(self):
        if self.unit_form.is_valid():
            self.unit_form.save()
            return True
        return False


class UnitCreateView(UnitCRUDView):
    """
    Class for Unit Create View
    """

    def get(self, *args, **kwargs):
        self._create_form()
        self._aggregate()
        return self._render()

    def post(self, *args, **kwargs):
        self._create_form()
        if self._validate_form():
            return self._redirect()
        self._aggregate()
        return self._render_content()


class UnitUpdateView(UnitCRUDView):
    """
    Class for Unit Update View
    """

    def get(self, *args, **kwargs):
        self._create_form()
        self._aggregate()
        return self._render()

    def post(self, *args, **kwargs):
        self._create_form()
        if self._validate_form():
            return self._redirect()
        self._aggregate()
        return self._render_content()


class UnitDeleteView(UnitCRUDView):
    """
    Class for Unit Delete View
    """

    kwargs_params_slots = {
        'id': [None, 0]
    }

    def _delete_unit(self):
        unit = self.UNIT_MODEL.filter(pk=self.params_storage['id']).first()
        if unit:
            unit.remove()

    def get(self, *args, **kwargs):
        self._delete_unit()
        self._aggregate()
        return self._render()

    def post(self, *args, **kwargs):
        self._create_form()
        if self._validate_form():
            return self._redirect()
        self._aggregate()
        return self._render_content()
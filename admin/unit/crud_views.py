# coding: utf-8


import json
import base64
import pymorphy2
import itertools
from django.shortcuts import HttpResponseRedirect, HttpResponse

from leon.base import BaseView, BaseParamsValidatorMixin
from .crud_extra import create_unit_extra
from .format_widgets import FormFormatWidget


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


class UnitMasterCreateView(BaseView):
    """
    Class for Unit Create View
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
    develop_extra = None
    unit_extra = None

    FORM_FORMAT_WIDGET = FormFormatWidget

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
        super(UnitMasterCreateView, self).__init__(**kwargs)
        self.extra = {}

    @staticmethod
    def _get_obj_meta(obj):
        """
        Return Django obj private _meta field
        :type obj: object
        """
        return obj._meta

    @staticmethod
    def _get_obj_name(obj):
        """
        Return Django obj private __name
        :type obj: object
        """
        return obj.__name__

    def _model_form_header(self, form, status):
        """
        Create form header (using model form)
        :param form:
        :param action:
        :return:
        """
        morph = pymorphy2.MorphAnalyzer()
        model = self._get_obj_meta(form).model
        morph_obj = morph.parse(self._get_obj_meta(model).
                                verbose_name.lower())[0]
        return '{} {}'.format(self.unit_extra[status]['header_pfx'],
                              morph_obj.inflect({'gent'}).word)

    def _create_master_form(self, get=True):
        form = self.master_form_class() if get \
            else self.master_form_class(json.loads(self.params_storage['data']))
        self.master_form = {
            'form': form,
            'header': self._model_form_header(form, 'master')
        }

    def _create_slave_form_s(self):
        self.slave_form_s = []
        for slave_form_class in self.slave_form_class_s:
            slave_form = slave_form_class()
            self.slave_form_s.append({
                'form': slave_form,
                'header': self._model_form_header(slave_form, 'slave')
            })

    def _create_meta(self):
        self.unit_meta = json.dumps(self.develop_extra['meta'])

    def _create_breadcrumb(self):
        pass

    def _format_master_form(self):
        self.unit_master_form = self.FORM_FORMAT_WIDGET().format(self.master_form['form'],
                                                                 self.master_form['header'],
                                                                 'master_form',
                                                                 self.extra['master_form']['groups'],
                                                                 self.extra['master_form']['buttons'],
                                                                 self.extra['subtype'],
                                                                 None)

    def _format_slave_form_s(self):
        self.unit_slave_form_s = []
        for slave_obj, slave_extra in itertools.zip_longest(self.slave_form_s,
                                                            self.extra['slave_form_s']):
            form = self.FORM_FORMAT_WIDGET().format(slave_obj['form'],
                                                    slave_obj['header'],
                                                    '{}_form'.format(slave_extra['field']),
                                                    slave_extra['groups'],
                                                    slave_extra['buttons'],
                                                    self.extra['subtype'],
                                                    None)
            self.unit_slave_form_s.append(form)

    def _format_breadcrumb(self):
        pass

    def _redirect(self):
        return HttpResponse(json.dumps({'url': self.redirect_url}))

    def _render_content(self):
        response = self._render()
        html = response.content
        return HttpResponse(json.dumps({'url': None,
                                        'html': html.decode('utf-8')}))

    def _validate_master_form(self):
        if self.master_form['form'].is_valid():
            self.master_form['form'].save()
            return True

    def get(self, *args, **kwargs):
        self._create_breadcrumb()
        self._create_master_form()
        self._create_slave_form_s()
        self._create_meta()

        self._convert_extra()

        self._format_master_form()
        self._format_slave_form_s()
        # self._format_meta()
        self._format_breadcrumb()

        self._aggregate()
        return self._render()

    def post(self, *args, **kwargs):
        self._create_breadcrumb()
        self._create_master_form(get=False)
        if self._validate_master_form():
            return self._redirect()
        self.master_form['form'].save()
        self._create_slave_form_s()
        self._create_meta()
        #
        self._format_master_form()
        self._format_slave_form_s()
        # self._format_meta()
        self._format_breadcrumb()

        self._aggregate()
        return self._render_content()

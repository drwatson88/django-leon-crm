# coding: utf-8


import pymorphy2
from leon.base import BaseView, BaseParamsValidatorMixin


class UnitMasterFormatMixin(object):

    def _format(self):
        pass


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


class UnitMasterCreateView(BaseView):

    """
    Class for Unit Create View
    (use in parent factory class)
    """

    kwargs_params_slots = {
        'pk': [None, ''],
    }

    request_params_slots = {
    }

    session_params_slots = {

    }

    template_name = None
    model = None
    master_form_class = None
    slave_form_class_s = None
    develop_extra = None
    unit_extra = None

    def __init__(self, **kwargs):
        """

        :param kwargs:
        """
        self.params_storage = {}
        self.output_context = {
            'unit_master_form': None,
            'unit_child_form_s': None,
            'unit_meta': None
        }
        super(UnitMasterCreateView, self).__init__(**kwargs)

    def _create_master_form(self):
        self.master_form = self.master_form_class()

        morph = pymorphy2.MorphAnalyzer()
        morph_obj = morph.parse(self.model.Meta.verbose_name.lower())[0]
        self.master_form_header = morph_obj.inflect({'gent'}).word

    def _create_slave_form_s(self):
        self.slave_form_s = []
        for slave_form_class in self.slave_form_class_s:
            slave_form = slave_form_class()
            self.slave_form_s.append(slave_form)

    def _create_meta(self):
        pass

    def _format_master_form(self):
        self.unit_master_form = {
            'header': self.master_form_header,
            'items': [{
                'name': field,
                'id': 'id_{}'.format(field),
                'slave_button': None,
                'attributes': self.master_form[field].field.widget.attrs,
                'type': self.master_form[field].field.input_type,
                      } for field in self.master_form.fields],
            'master_buttons': None
        }

    def _format_child_form_s(self):
        pass

    def get(self, *args, **kwargs):
        self._create_master_form()
        self._create_slave_form_s()
        self._create_meta()

        self._format_master_form()
        self._format_child_form_s()
        # self._format_meta()

        self._aggregate()
        return

    def post(self, *args, **kwargs):

        # self._format_master_form()
        # self._format_child_form_s()
        # self._format_meta()

        self._aggregate()
        return

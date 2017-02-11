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
            'unit_slave_form_s': None,
            'unit_meta': None
        }
        super(UnitMasterCreateView, self).__init__(**kwargs)

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

    @staticmethod
    def _get_field_attr(form, field):
        return form[field].field.widget.attrs

    @staticmethod
    def _get_field_type(form, field):
        return form[field].field.widget.input_type

    def _model_form_header(self, form, action):
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
        return '{} {}'.format(self.unit_extra['header'][action],
                              morph_obj.inflect({'gent'}).word)

    def _create_master_form(self, get=True):
        form = self.master_form_class() if get \
            else self.master_form_class(self.params_storage['master_form'])
        self.master_form = {
            'form': form,
            'header': self._model_form_header(form, 'create')
        }

    def _create_slave_form_s(self):
        self.slave_form_s = []
        for slave_form_class in self.slave_form_class_s:
            slave_form = slave_form_class()
            self.slave_form_s.append({
                'form': slave_form,
                'header': self._model_form_header(slave_form, 'create')
            })

    def _create_meta(self):
        pass

    def _create_breadcrumb(self):
        pass

    def _format_master_form(self):
        form = self.master_form['form']
        self.unit_master_form = {
            'header': self.master_form['header'],
            'css_class': 'master_form',
            'groups': [
                {
                    'items': [
                        {
                            'name': field,
                            'css_class': '{}'.format(field),
                            'slave_button': True if field in self.develop_extra['brackets']
                            else False,
                            'attributes': self._get_field_attr(form, field),
                            'type': 'input-{}'.format(self._get_field_type(form, field)),
                            'subtype': 'a',
                            "col_md": 12
                        }
                    ]
                } for field in form.fields
            ],
            'buttons': [
                {
                    'href': '#',
                    'title': 'Назад'
                },
                {
                    'href': '#',
                    'title': 'Сохранить'
                }
            ]
        }

    def _format_slave_form_s(self):
        self.unit_slave_form_s = []
        for slave_form in self.slave_form_s:
            form = slave_form['form']
            model = self._get_obj_meta(form).model
            model_name = self._get_obj_name(model).lower()
            self.unit_slave_form_s.append({
                'header': slave_form['header'],
                'css_class': '{}_form'.format(model_name),
                'groups': [
                    {
                        'items': [
                            {
                                'name': field,
                                'css_class': '{}'.format(field),
                                'attributes': self._get_field_attr(form, field),
                                'type': 'input-{}'.format(self._get_field_type(form, field)),
                                'subtype': 'a',
                                "col_md": 12
                            }
                        ]
                    } for field in form.fields
                ],
                'buttons': [
                    {
                        'href': '#',
                        'title': 'Добавить'
                    }
                ]
            })

    def _format_breadcrumb(self):
        pass

    def get(self, *args, **kwargs):
        self._create_breadcrumb()
        self._create_master_form()
        self._create_slave_form_s()
        self._create_meta()

        self._format_master_form()
        self._format_slave_form_s()
        # self._format_meta()
        self._format_breadcrumb()

        self._aggregate()
        return self._render()

    def post(self, *args, **kwargs):
        self._create_breadcrumb()
        self._create_master_form(get=False)
        self._create_slave_form_s()
        self._create_meta()

        self._format_master_form()
        self._format_slave_form_s()
        # self._format_meta()
        self._format_breadcrumb()

        self._aggregate()
        return

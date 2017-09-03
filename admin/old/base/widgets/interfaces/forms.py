# -*- coding: utf-8 -*-


import itertools
import pymorphy2
from django.forms import widgets


class FormWidgetInterface(object):

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
    def _get_button(slave_button, subtype):
        """
        """
        return {
            'title': slave_button.get('title'),
            'href': slave_button.get('href'),
            'css_class': slave_button.get('css_class'),
            'subtype': subtype
        }

    @staticmethod
    def _get_field_col(index, col_sizes):
        """
        """
        return int((col_sizes[index] * 12) / sum(col_sizes))

    def _format_field(self, field):
        field_type = self._get_field_type(field)
        return getattr(self, '_input_{}'.format(field_type))(field)

    def _get_field_label(self, field):
        """
        """
        return self[field].field.label

    def _get_field_value(self, field):
        """
        """
        return self[field].initial or self[field].data or ''

    def _get_field_errors(self, field):
        """
        """
        return self[field].errors or []

    def _get_field_attr(self, field):
        """
        """
        return self[field].field.widget.attrs

    def _get_field_type(self, field):
        """
        """
        if isinstance(self[field].field.widget, widgets.TextInput):
            return 'text'
        if isinstance(self[field].field.widget, widgets.Select):
            return 'select'
        if isinstance(self[field].field.widget, widgets.Textarea):
            return 'textarea'
        if isinstance(self[field].field.widget, widgets.ClearableFileInput):
            return 'file'
        if isinstance(self[field].field.widget, widgets.CheckboxInput):
            return 'checkbox'

    def _get_input_select_items(self, field):
        for name, value in self[field].field.widget.choices:
            yield name, value

    def _input_select(self, field):
        """
        :return:
        """
        return {
            'name': field,
            'label': self._get_field_label(field),
            'css_class': '{}'.format(field),
            'attributes': self._get_field_attr(field),
            'items': [
                {
                    'name': name,
                    'value': value
                } for value, name in self._get_input_select_items(field)
            ]
        }

    def _input_text(self, field):
        """
        :return:
        """
        return {
            'name': field,
            'label': self._get_field_label(field),
            'value': self._get_field_value(field),
            'css_class': '{}'.format(field),
            'attributes': self._get_field_attr(field),
            'errors': self._get_field_errors(field)
        }

    def _input_textarea(self, field):
        """
        :return:
        """
        return {
            'name': field,
            'label': self._get_field_label(field),
            'value': self._get_field_value(field),
            'css_class': '{}'.format(field),
            'attributes': self._get_field_attr(field)
        }

    def _input_checkbox(self, field):
        """
        :return:
        """
        return {
            'name': field,
            'label': self._get_field_label(field),
            'value': self._get_field_value(field),
            'css_class': '{}'.format(field),
            'attributes': self._get_field_attr(field)
        }

    def _get_group_items(self, group):
        """
        :return:
        """
        return [
            {
                'input': self._format_field(field),
                'type': 'input-{}'.format(self._get_field_type(field)),
                'col_size': self._get_field_col(index, group['col_sizes']),
                'subtype': self.Options.subtype
            } for field, index in itertools.zip_longest(group['items'],
                                                        range(len(group['items'])))
        ]

    def css_class(self):
        return getattr(self.Options, 'css_class', '')

    def header(self):
        """
        Create form header (using model form)
        :return:
        """
        morph = pymorphy2.MorphAnalyzer()
        model = self._get_obj_meta(self).model
        morph_obj = morph.parse(self._get_obj_meta(model).
                                verbose_name.lower())[0]
        return '{} {}'.format(self.Options.header_pfx,
                              morph_obj.inflect({'gent'}).word)

    def hidden(self):
        """
        Create form hidden (using model form)
        :return:
        """
        return getattr(self.Options, 'hidden', False)

    def groups(self):
        """
        :return:
        """
        return [
            {
                'items': self._get_group_items(group),
                'slave_buttons': [
                    {
                        'title': getattr(self.Options, 'slave_button_title', ''),
                        'css_class': group['items'][-1],
                        'subtype': 'a'
                    }
                ] if group.get('slave_button') else []
            } for group in self.Options.groups
        ]

    def buttons(self):
        """
        :return:
        """

        return self.Options.main_buttons

    def message(self):
        """
        :return:
        """

        return self.Options.message


class FilterWidgetInterface(object):

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
    def _get_button(slave_button, subtype):
        """
        """
        return {
            'title': slave_button.get('title'),
            'href': slave_button.get('href'),
            'css_class': slave_button.get('css_class'),
            'subtype': subtype
        }

    @staticmethod
    def _get_field_col(index, col_sizes):
        """
        """
        return int((col_sizes[index] * 12) / sum(col_sizes))

    def _format_field(self, field):
        field_type = self._get_field_type(field)
        return getattr(self, '_input_{}'.format(field_type))(field)

    def _get_field_label(self, field):
        """
        """
        return self[field].field.label

    def _get_field_value(self, field):
        """
        """
        return self[field].initial or ''

    def _get_field_attr(self, field):
        """
        """
        return self[field].field.widget.attrs

    def _get_field_type(self, field):
        """
        """
        if isinstance(self[field].field.widget, widgets.TextInput):
            return 'text'
        if isinstance(self[field].field.widget, widgets.Select):
            return 'select'

    def _get_input_select_items(self, field):
        for name, value in self[field].field.widget.choices:
            yield name, value

    def _input_select(self, field):
        """
        :return:
        """
        return {
            'name': field,
            'label': self._get_field_label(field),
            'css_class': '{}'.format(field),
            'attributes': self._get_field_attr(field),
            'items': [
                {
                    'name': name,
                    'value': value
                } for value, name in self._get_input_select_items(field)
            ]
        }

    def _input_text(self, field):
        """
        :return:
        """
        return {
            'name': field,
            'label': self._get_field_label(field),
            'value': self._get_field_value(field),
            'css_class': '{}'.format(field),
            'attributes': self._get_field_attr(field)
        }

    def _get_group_items(self, group):
        """
        :return:
        """
        return [
            {
                'input': self._format_field(field),
                'type': 'input-{}'.format(self._get_field_type(field)),
                'col_size': self._get_field_col(index, group['col_sizes']),
                'subtype': self.Options.subtype
            } for field, index in itertools.zip_longest(group['items'],
                                                        range(len(group['items'])))
        ]

    def css_class(self):
        return getattr(self.Options, 'css_class', '')

    def header(self):
        """
        Create form header (using model form)
        :return:
        """
        return self.Options.header

    def hidden(self):
        """
        Create form hidden (using model form)
        :return:
        """
        return getattr(self.Options, 'hidden', False)

    def groups(self):
        """
        :return:
        """
        return [
            {
                'items': self._get_group_items(group),
                'slave_buttons': [
                    {
                        'title': getattr(self.Options, 'slave_button_title', ''),
                        'css_class': group['items'][-1],
                        'subtype': 'a'
                    }
                ] if group.get('slave_button') else []
            } for group in self.Options.groups
        ]

    def buttons(self):
        """
        :return:
        """

        return self.Options.main_buttons

    def message(self):
        """
        :return:
        """

        return

# coding: utf-8


import itertools


# class UnitMasterFormatMixin(object):
#     """
#     Class for Unit Format data
#     """
#
#
#
#     @staticmethod
#     def _get_field_attr(form, field):
#         """
#         Return Django obj private __name
#         :type obj: object
#         """
#         return form[field].field.widget.attrs
#
#     @staticmethod
#     def _get_field_type(form, field):
#         """
#         Return Django obj private __name
#         :type obj: object
#         """
#         return form[field].field.widget.input_type
#
#     @staticmethod
#     def _get_field_label(form, field):
#         """
#         Return Django obj private __name
#         :type obj: object
#         """
#         return form[field].field.label
#
#     @staticmethod
#     def _get_field_value(form, field):
#         """
#         Return Django obj private __name
#         :type obj: object
#         """
#         return form[field].value() if form[field].value() else ''
#
#     @staticmethod
#     def _get_field_errors(form, field):
#         """
#         Return Django obj private __name
#         :type obj: object
#         """
#         return form.errors.get(field, [])
#
#     def _get_field_col(self, field, group):
#         """
#         Return Django obj private __name
#         :type obj: object
#         """
#         if field in self.develop_extra['brackets']:
#             return 9
#         return 6 if len(group) > 1 else 12
#
#     def _get_slave_button(self, group):
#         """
#         Return Django obj private __name
#         :type obj: object
#         """
#         if group[0] in self.develop_extra['brackets']:
#             return {"title": self.unit_extra['master']['slave_buttons']['meta']['title'],
#                     "subtype": self.develop_extra['app_widget_subtype'],
#                     "href": self.develop_extra['slave_buttons'][group[0]]['href'],
#                     'css_class': group[0]}
#         else:
#             return False
#
#     def _get_button_href(self, button_name):
#         """
#         Return Django obj private __name
#         :type obj: object
#         """
#         return self.develop_extra['master_buttons'][button_name]['href'] \
#             if self.develop_extra['master_buttons'].get(button_name) else '#'
#
#     def _format_master_form(self):
#         """
#         Return Django obj private __name
#         :type obj: object
#         """
#         form = self.master_form['form']
#         self.unit_master_form = {
#             'header': self.master_form['header'],
#             'css_class': 'master_form',
#             'groups': [
#                 {
#                     'items': [
#                         {
#                             'name': field,
#                             'label': self._get_field_label(form, field),
#                             'css_class': '{}'.format(field),
#                             'value': self._get_field_value(form, field),
#                             'errors': self._get_field_errors(form, field),
#                             'attributes': self._get_field_attr(form, field),
#                             'type': 'input-{}'.format(self._get_field_type(form, field)),
#                             'subtype': self.develop_extra['app_widget_subtype'],
#                             'col_md': self._get_field_col(field, group)
#                         } for field in group
#                     ],
#                     'slave_button': self._get_slave_button(group)
#                 } for group in self.develop_extra['master_groups']
#             ],
#             'buttons': [{
#                 'css_class': button['css_class'],
#                 'title': button['title'],
#                 'href': self._get_button_href(button['key'])
#                         } for button in self.unit_extra['master']['main_buttons']['items']]
#         }
#
#     def _format_slave_form_s(self):
#         """
#         Return Django obj private __name
#         :type obj: object
#         """
#         self.unit_slave_form_s = []
#         for slave_form in self.slave_form_s:
#             form = slave_form['form']
#             model = self._get_obj_meta(form).model
#             model_name = self._get_obj_name(model).lower()
#             self.unit_slave_form_s.append({
#                 'hidden': True,
#                 'header': slave_form['header'],
#                 'css_class': '{}_form'.format(model_name),
#                 'groups': [
#                     {
#                         'items': [
#                             {
#                                 'name': field,
#                                 'label': self._get_field_label(form, field),
#                                 'css_class': '{}'.format(field),
#                                 'attributes': self._get_field_attr(form, field),
#                                 'type': 'input-{}'.format(self._get_field_type(form, field)),
#                                 'subtype': self.develop_extra['app_widget_subtype'],
#                                 "col_md": self._get_field_col(field, group)
#                             } for field in group
#                         ]
#                     } for group in self.develop_extra['{}_groups'.format(model_name)]
#                 ],
#                 'buttons': [
#                     {
#                         'css_class': self.unit_extra['slave']['main_buttons']['meta']['css_class'],
#                         'href': self.develop_extra['slave_buttons'][model_name]['href'],
#                         'title': self.unit_extra['slave']['main_buttons']['meta']['title']
#                     }
#                 ],
#                 'message': {
#                     'success': "Объект успешно добавлен",
#                     'error': "Объект не добавлен"
#                 }
#             })
#
#     def _format_breadcrumb(self):
#         """
#         Return Django obj private __name
#         :type obj: object
#         """
#         pass


class FormatWidget(object):

    @staticmethod
    def _get_field_label(form, field):
        """
        """
        return form[field].field.label

    @staticmethod
    def _get_field_attr(form, field):
        """
        """
        return form[field].field.widget.attrs

    @staticmethod
    def _get_field_type(form, field):
        """
        """
        return form[field].field.widget.input_type


class InputTextFormatWidget(FormatWidget):

    def format(self, form, field):

        return {
            'name': field,
            'label': self._get_field_label(form, field),
            'css_class': '{}'.format(field),
            'attributes': self._get_field_attr(form, field)}


class InputFileFormatWidget(FormatWidget):

    def file(self):
        pass


class InputSelectFormatWidget(FormatWidget):

    def select(self):
        pass


class FormFormatWidget(FormatWidget):
    """
        Class for Form Builder
    """
    def __init__(self):
        self.input_text = InputTextFormatWidget
        self.input_select = InputSelectFormatWidget
        self.input_file = InputFileFormatWidget

    @staticmethod
    def _get_field_col(index, col_sizes):
        """
        """
        return int((col_sizes[index] * 12)/sum(col_sizes))

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

    def _format_field(self, form, field):
        field_type = self._get_field_type(form, field)
        format_widget = getattr(self, 'input_{}'.format(field_type))()
        return format_widget.format(form, field)

    def format(self, form, extra_header, extra_css_class, extra_groups,
               extra_buttons, extra_subtype, extra_message):
        format_form = {
            'hidden': True,
            'header': extra_header,
            'css_class': extra_css_class,
            'groups': [
                {
                    'items': [
                        {
                            'input': self._format_field(form, field),
                            'type': 'input-{}'.format(self._get_field_type(form, field)),
                            'col_size': self._get_field_col(index, group['col_sizes']),
                            'subtype': extra_subtype
                        } for field, index in itertools.zip_longest(group['items'],
                                                                    range(len(group['items'])))
                    ],
                    'slave_buttons': [
                        self._get_button(button, extra_subtype) for button in group['slave_buttons']
                    ]
                } for group in extra_groups
            ],
            'buttons': [
                self._get_button(button, extra_subtype) for button in extra_buttons
            ],
            'message': extra_message
        }
        return format_form


class FilterFormatWidget(FormatWidget):
    """
        Class for Filter Builder
    """
    def __init__(self):
        self.input_text = InputTextFormatWidget
        self.input_select = InputSelectFormatWidget
        self.input_file = InputFileFormatWidget

    @staticmethod
    def _get_field_col(index, col_sizes):
        """
        """
        return int((col_sizes[index] * 12)/sum(col_sizes))

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

    def _format_field(self, form, field):
        field_type = self._get_field_type(form, field)
        format_widget = getattr(self, 'input_{}'.format(field_type))()
        return format_widget.format(form, field)

    def format(self, form_filter, extra_header, extra_css_class, extra_groups,
               extra_buttons, extra_subtype, extra_message):
        format_filter = {
            'hidden': True,
            'header': extra_header,
            'css_class': extra_css_class,
            'groups': [
                {
                    'items': [
                        {
                            'input': self._format_field(form_filter, field),
                            'type': 'input-{}'.format(self._get_field_type(form_filter, field)),
                            'col_size': self._get_field_col(index, group['col_sizes']),
                            'subtype': extra_subtype
                        } for field, index in itertools.zip_longest(group['items'],
                                                                    range(len(group['items'])))
                    ]
                } for group in extra_groups
            ],
            'buttons': [
                self._get_button(button, extra_subtype) for button in extra_buttons
            ],
            'message': extra_message
        }
        return format_filter

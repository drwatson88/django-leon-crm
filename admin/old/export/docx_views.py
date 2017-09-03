# coding: utf-8


from django.http import HttpResponse

from leon.base import BaseView, BaseParamsValidatorMixin


class DocXParamsValidationMixin(BaseParamsValidatorMixin):
    """ Mixin with validators for validate
        request parameters.
    """
    @staticmethod
    def _order_validator(value, default):
        try:
            return int(value)
        except BaseException as exc:
            return default


class FileView(BaseView, DocXParamsValidationMixin):

    """
    Class for Docx View
    (use in parent factory class)
    """

    kwargs_params_slots = {
    }

    request_params_slots = {
        'order': [None, 1]
    }

    doc_format_class = None
    doc_string_template = None
    doc_struct_template = None
    template_pattern = None

    def __init__(self, **kwargs):
        """
        :param kwargs:
        """
        self.params_storage = {}
        self.output_context = {
            'doc': None,
        }
        super(FileView, self).__init__(**kwargs)

    def _create_data(self):
        self.data = {}

    def _create_document(self):
        self.doc = self.doc_format_class(self.doc_string_template,
                                         self.doc_struct_template,
                                         self.template_pattern.
                                         format(order=self.params_storage['order']),
                                         self.data).create_document()

    def _render(self):
        """
        :return:
        """
        response = HttpResponse(content_type='text/html')
        with open(self.doc[0], 'rb') as f:
            response.write(f.read())
        response['Content-Disposition'] = 'attachment; filename={attach_file}'.\
            format(attach_file=self.doc[1])
        return response

    def get(self, *args, **kwargs):
        self._create_data()
        self._create_document()
        self._aggregate()
        return self._render()

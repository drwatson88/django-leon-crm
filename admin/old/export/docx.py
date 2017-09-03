# coding: utf-8


import os
from zipfile import ZipFile
import settings


class DocXFormat(object):

    def __init__(self, string_template, struct_name, result_name, data):
        self.string_template = string_template
        self.struct_name = struct_name
        self.result_name = result_name
        self.data = data

    def _create_file(self):
        # Формирование файлов
        with open(os.path.join(settings.ADMIN_DOC_STRING_TEMPLATE_DIR,
                               self.string_template), 'r') as t:
            with open(os.path.join(settings.ADMIN_DOC_STRUCT_TEMPLATE_DIR,
                                   self.struct_name,
                                   'word',
                                   'document.xml'), 'w') as doc:
                # doc.write(t.read().format(**self.data).encode('utf-8'))
                doc.write(t.read())

        with ZipFile(os.path.join(settings.ADMIN_DOC_RESULT_DIR,
                                  self.result_name), 'w') as doc:
            for root, dirs, files in os.walk(os.path.join(settings.ADMIN_DOC_STRUCT_TEMPLATE_DIR,
                                                          self.struct_name)):
                for f in files:
                    arcname = os.path.join(os.path.relpath(root,
                                                           os.path.join(settings.ADMIN_DOC_STRUCT_TEMPLATE_DIR,
                                                                        self.struct_name)), f)
                    doc.write(
                        filename=os.path.join(root, f),
                        arcname=arcname
                    )
        return os.path.join(settings.ADMIN_DOC_RESULT_DIR,
                            self.result_name), self.result_name

    def create_document(self):
        return self._create_file()


# coding: utf-8


import pymorphy2


class BreadcrumbMixin(object):

    def _create_breadcrumb(self):
        self.breadcrumb = self.breadcrumb_page

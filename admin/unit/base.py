# -*- coding: utf-8 -*-


import pymorphy2

from functools import update_wrapper
import json
from django import forms
from django.views.generic import View
from django.views.generic import CreateView, \
    UpdateView, DetailView, DeleteView
from django.utils.decorators import classonlymethod


# class BaseCharButtonField(forms.CharField):
#
#     def __init__(self, *args, **kwargs):
#         button_options = kwargs.get('button')
#         if button_options:
#             del kwargs['button']
#         super(BaseCharButtonField, self).__init__(*args, **kwargs)
#         self.button = None


class BaseFormMixin(object):

    def __init__(self, *args, **kwargs):
        super(BaseFormMixin, self).__init__(*args, **kwargs)
        self._set_relations()

    def _set_relations(self):
        pass

    # def _set_base_buttons(self):
    #     self.base_button = self.button_map[self.action]


class BaseViewMixin(object):

    def get_context_data(self, **kwargs):
        context = super(BaseViewMixin, self).get_context_data(**kwargs)

        self._set_titles()
        self._set_meta()
        context.update({
            'extra_title': '{} {}'.format(self.title_map[self.action], self.title),
            'meta': json.dumps(self.meta)
        })
        return context

    def _set_titles(self):
        morph = pymorphy2.MorphAnalyzer()
        morph_obj = morph.parse(self.title)[0]
        self.title = morph_obj.inflect({'gent'}).word

    def _set_meta(self):
        self.meta = {}
        self.meta.update({
            'action': self.action,
            'section': self.section,
            'autocomplete': self.autocomplete,
            'validators': self.validators
        })

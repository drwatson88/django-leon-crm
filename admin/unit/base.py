# -*- coding: utf-8 -*-


import pymorphy2

from functools import update_wrapper
import json
from django import forms
from django.views.generic import View
from django.views.generic import CreateView, \
    UpdateView, DetailView, DeleteView
from django.utils.decorators import classonlymethod


class BaseCharButtonField(forms.CharField):

    def __init__(self, *args, **kwargs):
        button_options = kwargs.get('button')
        if button_options:
            del kwargs['button']
        super(BaseCharButtonField, self).__init__(*args, **kwargs)
        self.button = None


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


class BaseViewFactory(View):

    """ Class Base Dispatcher. Use for CRUD actions.
        We generate CRUD four bandit classes in one
        controller.
    """

    create_view_class = CreateView
    update_view_class = UpdateView
    detail_view_class = DetailView
    delete_view_class = DeleteView

    create_mixin = []
    update_mixin = []
    detail_mixin = []
    delete_mixin = []

    view_internal_mixin = [BaseViewMixin]
    form_internal_mixin = [BaseFormMixin]

    action = None
    model = None
    form_class = None
    success_url = None
    fields = None
    title_map = {
        'create': 'Добавление',
        'update': 'Просмотр/Редактирование',
        'delete': 'Удаление'
    }
    title = None
    button_map = {
        'create': [
            {
                'title': 'Назад',
                'type': 'link',
                'disabled': False
            },
            {
                'title': 'Сохранить',
                'type': 'submit',
                'disabled': True
            }
        ],
        'update': [
            {
                'title': 'Назад',
                'type': 'link',
                'disabled': False
            },
            {
                'title': 'Сохранить',
                'type': 'submit',
                'disabled': True
            }
        ],
        'delete': {}
    }
    section = None
    autocomplete = None
    validators = None
    template_name = 'crm/blocks/unit/inside/sample.html'

    @classonlymethod
    def as_view(cls, **initkwargs):
        """
        Main entry point for a request-response process.
        """
        for key in initkwargs:
            if key in cls.http_method_names:
                raise TypeError("You tried to pass in the %s method name as a "
                                "keyword argument to %s(). Don't do that."
                                % (key, cls.__name__))
            if not hasattr(cls, key):
                raise TypeError("%s() received an invalid keyword %r. as_view "
                                "only accepts arguments that are already "
                                "attributes of the class." % (cls.__name__, key))

        def form_create(action):
            form_internal_mixin = getattr(cls, 'form_internal_mixin')
            form_siblings = []
            form_siblings.extend(form_internal_mixin)
            form_siblings.extend([cls.form_class])
            form_namespace = {
                'base_buttons': cls.button_map[action],
            }
            return type('FormClass', tuple(form_siblings), form_namespace)

        def view_create(action, form_class):
            view_parent = getattr(cls, '{}_view_class'.format(action))
            view_mixin = getattr(cls, '{}_mixin'.format(action))
            view_internal_mixin = getattr(cls, 'view_internal_mixin')
            view_namespace = {
                'form_class': form_class,
                'template_name': cls.template_name,
                'success_url': cls.success_url,
                'model': cls.model,
                'fields': cls.fields,
                'title_map': cls.title_map,
                'title': cls.title,
                'action': action,
                'section': cls.section,
                'autocomplete': cls.autocomplete,
                'validators': cls.validators,
            }
            view_siblings = []
            view_siblings.extend(view_internal_mixin)
            view_siblings.extend([view_parent])
            view_siblings.extend(view_mixin)
            return type('TargetView', tuple(view_siblings), view_namespace)

        def router(**kwargs):
            action = kwargs['action']
            form_class = form_create(action)
            view_class = view_create(action, form_class)
            return view_class

        def view(request, *args, **kwargs):
            target_class = router(**kwargs)
            self = target_class(**initkwargs)
            if hasattr(self, 'get') and not hasattr(self, 'head'):
                self.head = self.get
            self.request = request
            self.args = args
            self.kwargs = kwargs
            return self.dispatch(request, *args, **kwargs)

        update_wrapper(view, cls, updated=())
        update_wrapper(view, cls.dispatch, assigned=())
        return view


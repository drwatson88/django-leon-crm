# coding: utf-8


from functools import update_wrapper

from django.utils.decorators import classonlymethod
from django.views.generic import View

from admin.base.widgets.mixins import UnitMasterFormMixin, UnitSlaveFormMixin
from .crud_views import UnitMasterCreateView, UnitMasterUpdateView, \
    UnitMasterParamsValidationMixin
from admin.base.widgets.interfaces import FormWidgetInterface, FilterWidgetInterface
from .crud_forms import UnitMasterFormWorkMixin


class BaseViewFactory(View):

    """ Class Base Dispatcher. Use for CRUD actions.
        We generate CRUD four bandit classes in one
        controller.
    """

    kwargs_params_slots = None
    request_params_slots = None

    create_view_class = UnitMasterCreateView
    update_view_class = UnitMasterUpdateView
    detail_view_class = None
    delete_view_class = None

    create_mixin = [UnitMasterParamsValidationMixin, UnitMasterFormMixin, UnitSlaveFormMixin]
    update_mixin = [UnitMasterParamsValidationMixin]
    detail_mixin = []
    delete_mixin = []

    view_internal_mixin = []
    create_master_form_internal_mixin = [FormWidgetInterface, UnitMasterFormWorkMixin]
    create_slave_form_internal_mixin = [FormWidgetInterface]

    update_master_form_internal_mixin = [FormWidgetInterface, UnitMasterFormWorkMixin]
    update_slave_form_internal_mixin = [FormWidgetInterface]

    create_redirect_url = None
    update_redirect_url = None

    action = None
    model = None
    master_form_class = None
    slave_form_class_s = None
    success_url = None
    fields = None
    title = None

    section = None
    meta = None
    template_name = None

    breadcrumb_page = None

    @classonlymethod
    def as_view(cls, load_action, **initkwargs):
        """
        Main entry point, when initialize urls (as_view child class return)
        :param load_action: crud action
        :param initkwargs: other params
        :return:
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

        def master_form_create(action):
            form_internal_mixin = getattr(cls, '{}_master_form_internal_mixin'.format(action))
            form_siblings = []
            form_siblings.extend(form_internal_mixin)
            form_siblings.extend([cls.master_form_class])
            form_namespace = {}
            return type('MasterFormClass', tuple(form_siblings), form_namespace)

        def slave_form_s_create(action):
            slave_form_internal_mixin = getattr(cls, '{}_slave_form_internal_mixin'.format(action))

            slave_form_s = []
            for form_class in cls.slave_form_class_s:
                form_siblings = []
                form_siblings.extend(slave_form_internal_mixin)
                form_siblings.extend([form_class])
                form_namespace = {}
                slave_form_s.append(type('SlaveFormClass', tuple(form_siblings), form_namespace))
            return slave_form_s

        def view_create(action, master_form_class, slave_form_class_s):
            view_parent = getattr(cls, '{}_view_class'.format(action))
            view_mixin = getattr(cls, '{}_mixin'.format(action))
            view_internal_mixin = getattr(cls, 'view_internal_mixin')
            view_namespace = {
                'master_form_class': master_form_class,
                'slave_form_class_s': slave_form_class_s,
                'template_name': cls.template_name,
                'success_url': cls.success_url,
                'model': cls.model,
                'redirect_url': getattr(cls, '{}_redirect_url'.format(action)),
                # 'fields': cls.fields,
                # 'title': cls.title,
                'action': action,
                'meta': cls.meta,
                'breadcrumb_page': cls.breadcrumb_page,
                # 'section': cls.section,
                # 'autocomplete': cls.autocomplete,
                # 'validators': cls.validators,
            }
            if cls.kwargs_params_slots:
                view_namespace.update({'kwargs_params_slots': cls.kwargs_params_slots})
            if cls.request_params_slots:
                view_namespace.update({'request_params_slots': cls.request_params_slots})
            view_siblings = []
            view_siblings.extend(view_internal_mixin)
            view_siblings.extend(view_mixin)
            view_siblings.extend([view_parent])
            return type('UnitView', tuple(view_siblings), view_namespace).as_view()

        def router(action):
            master_form_class = master_form_create(action)
            slave_form_class_s = slave_form_s_create(action)
            view_class = view_create(action, master_form_class, slave_form_class_s)
            return view_class

        return router(load_action)

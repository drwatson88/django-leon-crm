# coding: utf-8


import json
from django.shortcuts import HttpResponse
from leon.base import BaseView, BaseParamsValidatorMixin


class ObjLookupView(BaseView, BaseParamsValidatorMixin):

    """ Obj Search View.
    """

    request_params_slots = {
        'lookup': [None, '']
    }

    session_params_slots = {
    }

    session_save_slots = {
    }

    def __init__(self, *args, **kwargs):
        self.params_storage = {}
        self.output_context = {
            'lookup_obj_s': None,
        }
        super(ObjLookupView, self).__init__(*args, **kwargs)
        self.lookup_obj_s = None

    def _lookup(self):
        lookup_obj_s = None
        self.lookup_obj_s = lookup_obj_s[:15]

    def get(self, *args, **kwargs):
        self._lookup()
        super(ObjLookupView, self).get(*args, **kwargs)
        return HttpResponse(json.dumps(self.output_context))


class ObjCheckView(BaseView, BaseParamsValidatorMixin):

    """ City Search View.
    """

    request_params_slots = {
        'check': [None, '']
    }

    session_params_slots = {
    }

    session_save_slots = {
    }

    def __init__(self, *args, **kwargs):
        self.params_storage = {}
        self.output_context = {
            'check': None,
        }
        super(ObjCheckView, self).__init__(*args, **kwargs)
        self.check = None
        self.message = None

    def _check(self):
        check_obj_s = None
        self.check = True if check_obj_s else False
        self.message = None # 'Создайте объект с помощью кнопки "ДОБАВИТЬ"(+)'

    def get(self, *args, **kwargs):
        self._check()
        super(ObjCheckView, self).get(*args, **kwargs)
        return HttpResponse(json.dumps(self.output_context))

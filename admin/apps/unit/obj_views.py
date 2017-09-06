# coding: utf-8


import json
from django.shortcuts import HttpResponse
from django.db.models import Q

from leon.base import BaseView, BaseParamsValidatorMixin


class UnitObjParamsValidationMixin(BaseParamsValidatorMixin):
    """ Mixin with validators for validate
        request parameters.
    """

    @staticmethod
    def _pk_validator(value, default):
        try:
            return int(value)
        except BaseException as exc:
            return default

    @staticmethod
    def _lookup_validator(value, default):
        return value

    @staticmethod
    def _slave_validator(value, default):
        return value

    @staticmethod
    def _data_validator(value, default):
        return value


class ObjLookupView(BaseView, UnitObjParamsValidationMixin):

    """ Obj Search View.
    """

    request_params_slots = {
        'lookup': [None, []]
    }

    session_params_slots = {
    }

    session_save_slots = {
    }

    MODEL = None
    fields = []

    def __init__(self, *args, **kwargs):
        self.params_storage = {}
        self.output_context = {
            'lookup_obj_s': None,
        }
        super(ObjLookupView, self).__init__(*args, **kwargs)
        self.lookup_obj_s = None

    def _lookup(self):
        query = self.MODEL.objects

        q_chain = [Q(**{'{}__icontains'.format(f): self.params_storage['lookup']})
                   for f in self.fields]
        q = q_chain.pop()
        for item in q_chain:
            q |= item

        lookup_obj_s = [{
                            'pk': item['pk'],
                            'name': '||'.join([item[f] for f in self.fields])}
                        for item in list(query.filter(q).values('pk', *self.fields))]
        self.lookup_obj_s = lookup_obj_s[:15]

    def get(self, *args, **kwargs):
        self._lookup()
        self._aggregate()
        return HttpResponse(json.dumps(self.output_context))


class ObjAddView(BaseView, UnitObjParamsValidationMixin):

    """ City Search View.
    """

    request_params_slots = {
        'slave': [None, ''],
        'data': [None, {}]
    }

    session_params_slots = {
    }

    session_save_slots = {
    }

    FORM = None

    def __init__(self, *args, **kwargs):
        self.params_storage = {}
        self.output_context = {
            'error': None
        }
        super(ObjAddView, self).__init__(*args, **kwargs)
        self.obj = None
        self.message = None

    def _add(self):
        self.form = self.FORM(json.loads(self.params_storage['data']))
        if self.form.is_valid():
            self.form.save()
            self.error = 0
        else:
            self.error = 1

    def post(self, *args, **kwargs):
        self._add()
        self._aggregate()
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

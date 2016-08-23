# -*- coding: utf-8 -*-

import json
from leon.base import BaseView, ParamsValidatorMixin


class OrgParamsValidatorMixin(ParamsValidatorMixin):

    """ Mixin with validators for validate
        request parameters.
    """

    @staticmethod
    def _ajax_validator(value, default):
        try:
            return int(value)
        except BaseException as exc:
            return default


class OrgBaseView(BaseView):

    """ Class Base for all Catalog Class Views
        When request is received, then
    """

    pass

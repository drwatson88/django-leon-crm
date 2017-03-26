# coding: utf-8


class UnitMasterFormMixin(object):

    master_form_class = None

    def _create_master_form(self, data=None, get=True):
        self.unit_master_form = self.master_form_class() if get \
            else self.master_form_class(data)


class UnitSlaveFormMixin(object):

    slave_form_class_s = []

    def _create_slave_form_s(self):
        self.unit_slave_form_s = [slave_form_class()
                                  for slave_form_class in self.slave_form_class_s]

# coding: utf-8


import itertools


class UnitMasterFormWorkMixin(object):

    def save(self):
        """
        Save Mixin
        :return:
        """
        master_obj = super(UnitMasterFormWorkMixin, self).save(commit=False)
        for slave_field, unique_keys in self.Options.slaves.items():
            if self.cleaned_data[slave_field]:
                related_model = master_obj._meta.get_field(slave_field).related_model()
                obj_filter = {field: value for field, value in itertools.zip_longest(
                    unique_keys,
                    self.cleaned_data[slave_field].split('||'))}
                obj = related_model.__class__.objects.filter(**obj_filter).all()[0]
                setattr(master_obj, '{}_id'.format(slave_field), obj.id)
        master_obj.save()

# coding: utf-8


import itertools


class UnitMasterFormWorkMixin(object):

    def save(self):
        """
        Save Mixin
        :return:
        """
        master_obj = super(UnitMasterFormWorkMixin, self).save(commit=False)

        brackets = [i for i in self.develop_extra['brackets']]
        for br in brackets:
            if self.cleaned_data[br]:
                related_model = master_obj._meta.get_field(br).related_model()
                obj_filter = {field: value for field, value in itertools.zip_longest(
                    self.develop_extra['unique_keys'][br], self.cleaned_data[br].split('||'))}
                obj = related_model.__class__.objects.get(**obj_filter)
                setattr(master_obj, '{}_id'.format(br), obj.id)
        master_obj.save()

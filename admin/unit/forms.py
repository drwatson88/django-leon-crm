# coding: utf-8


class MasterCreateFormMixin(object):

    def save(self):
        obj = super(MasterCreateFormMixin, self).save()

        brackets = [i for i in self.develop_extra['brackets']]
        for br in brackets:
            if self.cleaned_data[br]:
                fields = {self.cleaned_data[br]}

                related_model = obj._meta.get_field(br).related_model()
                related_model.objects.get()

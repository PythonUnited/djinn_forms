from django import forms
from djinn_forms.fields.relate import RelateField


class RelateMixin(object):

    """ When using relate fields, handle these in the save """

    def save_relations(self):

        for f_name, field in self.fields.items():
            if isinstance(field, RelateField):

                val = self.cleaned_data.get(f_name, {'rm': [], 'add': []})
                field.save_relations(self.instance, val)

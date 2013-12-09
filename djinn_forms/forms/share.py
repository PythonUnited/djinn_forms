from django import forms
from djinn_forms.fields.share import ShareField


class ShareMixin(object):

    """ When using share fields, handle these in the save """

    def save_shares(self, commit=True):

        # for ctype, cid, mode in self.cleaned_data['shares']['rm']:
        #     obj.rm_share(ctype, cid, mode)
        #
        # for ctype, cid, mode in self.cleaned_data['shares']['add']:
        #     obj.add_share(ctype, cid, mode)


        for f_name, field in self.fields.items():
            if isinstance(field, ShareField):

                val = self.cleaned_data.get(f_name, {'rm': [], 'add': []})
                field.save_share(self.instance, val, commit)

    def init_share_fields(self):

        for f_name, field in self.fields.items():
            if isinstance(field, ShareField):
                self.fields[f_name].instance = self.instance

from django.forms.widgets import Widget
from django.utils.safestring import mark_safe
from django.template.loader import render_to_string
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from djinn_contenttypes.utils import urn_to_object


class RelateWidget(Widget):

    """ Widget for handling relations to other content.
    The following extra attributes are supported:
     * content_types Allowed content types for this relation as list
     * relation_type Relation type to use for creating the actual relation
     * searchfield Look for this field in the searchengine

    To actually save the data that this widget produces, you need to
    make your form extend the djinn_forms.forms.RelateMixin and call
    the methods in that form.

    TODO: add unique settings
    TODO: add single select setting
    """

    template_name = 'djinn_forms/snippets/relatewidget.html'

    def value_from_datadict(self, data, files, name):

        """ The data may contain a list of objects to remove, and
        objects to add. Both are prefixed by the field name. The
        returned value is a dict with 'rm' and 'add' lists, that list
        the """

        result = {'rm': [], 'add': []}

        for item in data.get("%s_rm" % name, "").split(";;"):

            obj = urn_to_object(item)

            if obj:
                result['rm'].append(obj)

        for item in data.get("%s_add" % name, "").split(";;"):

            obj = urn_to_object(item)

            if obj:
                result['add'].append(obj)

        return result

    def build_attrs(self, extra_attrs=None, **kwargs):

        final_attrs = super(RelateWidget, self).build_attrs(
            extra_attrs=extra_attrs, **kwargs)

        url = self.attrs.get("search_url", reverse("djinn_forms_relatesearch"))
        url = "%s?content_types=%s&searchfield=%s" % (
            url,
            ",".join(self.attrs['content_types']),
            self.attrs.get("searchfield", "title_auto")
            )
        
        final_attrs.update(
            {'search_minlength': self.attrs.get("search_minlength", 2),
             'search_url': url,
             'multiple': True
             })
        
        return final_attrs
    
    def render(self, name, value, attrs=None):

        final_attrs = self.build_attrs(attrs, name=name, value=value)

        html = render_to_string(self.template_name, final_attrs)

        return mark_safe(u"".join(html))


class RelateSingleWidget(RelateWidget):

    """ Relate widget where only one relation is allowed """

    template_name = 'djinn_forms/snippets/relatesinglewidget.html'

    def value_from_datadict(self, data, files, name):

        """ The data may contain a list of objects to remove, and
        objects to add. Both are prefixed by the field name. The
        returned value is a dict with 'rm' and 'add' lists, that list
        the """

        result = super(RelateSingleWidget, self).value_from_datadict(
            data, files, name)

        result = result.get('add', [])

        if len(result):
            return result[0]
        else:
            return None

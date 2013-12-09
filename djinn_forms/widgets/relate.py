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

     TODO: add unique settings
     TODO: add single select setting
     TODO: select on 'select'
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

    def render(self, name, value, attrs=None):

        url = self.attrs.get("search_url", reverse("djinn_forms_relatesearch"))
        url = "%s?content_types=%s&searchfield=%s" % (
            url,
            ",".join(self.attrs['content_types']),
            self.attrs.get("searchfield", "title")
            )

        context = {'name': name,
                   'hint': self.attrs.get("hint", ""),
                   # Translators: djinn_forms relate add button label
                   'add_label': self.attrs.get("add_label", _("Add")),
                   'value': value,
                   'search_minlength': self.attrs.get("search_minlength", 2),
                   'search_url': url
                   }

        html = render_to_string(self.template_name, context)

        return mark_safe(u"".join(html))


class SingleRelateWidget(RelateWidget):

    """ Relate widget where only one relation is allowed """

    template_name = 'djinn_forms/snippets/singlerelatewidget.html'

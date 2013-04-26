from django.forms.widgets import Widget
from django.utils.safestring import mark_safe
from django.template.loader import render_to_string
from djinn_contenttypes.utils import get_object_by_ctype_id, object_to_urn, \
    urn_to_object


class LinkWidget(Widget):

    """ Link widget for internal and external links """

    def value_from_datadict(self, data, files, name):

        value = data[name].split("::")

        if len(value) == 3:
            obj = get_object_by_ctype_id(value[1], value[2])
            return object_to_urn(obj)
        else:
            return value[0]

    def render(self, name, value, attrs=None):

        if value.startswith("urn"):
            lexval = urn_to_object(value).title
        else:
            lexval = value

        context = {'name': name,
                   'lexical_value': lexval,
                   'value': value or "",
                   }

        html = render_to_string('djinn_forms/snippets/link_widget.html', 
                                context)
        
        return mark_safe(u"".join(html))

from django.forms.widgets import Widget
from django.utils.safestring import mark_safe
from django.template.loader import render_to_string
from django.core.urlresolvers import reverse


TPL = 'djinn_forms/snippets/relatewidget.html'


class RelateWidget(Widget):

    """ Widget for handling relations to other content.
    The following extra attributes are supported:
     * content_types Allowed content types for this relation
     * relation_type Relation type to use for creating the actual relation
     * src_obj Source object for relation
    """

    def __init__(self, src_obj=None, content_types="",
                 relation_type="", attrs=None):

        super(RelateWidget, self).__init__(attrs=attrs)
        self.relation_type = relation_type
        self.src_obj = src_obj
        self.content_types = content_types

    def value_from_datadict(self, data, files, name):

        """ The data may contain a list of objects to remove, and
        objects to add. Both are prefixed by the field name. The
        returned value is a dict with 'rm' and 'add' lists, that list
        the """

        result = {'rm': [], 'add': []}

        for item in data.get("%s_rm" % name, "").split(";;"):
            pair = item.split(":")
            if len(pair) == 2:
                result['rm'].append(pair)

        for item in data.get("%s_add" % name, "").split(";;"):
            pair = item.split(":")
            if len(pair) == 2:
                result['add'].append(pair)

        return result

    def render(self, name, value, attrs=None):

        context = {'name': name,
                   'label': self.label,
                   'hint': self.attrs.get("hint", ""),
                   'value': value or "",
                   'search_minlength': self.attrs.get("search_minlength", 2),
                   'search_url':
                   self.attrs.get("search_url",
                                  reverse("pgsearch_autocomplete"))
                   }

        context.update(self.__dict__)

        context['restrict_content_types'] = \
            ",".join(context.get('content_types', []))

        html = render_to_string(TPL, context)

        return mark_safe(u"".join(html))

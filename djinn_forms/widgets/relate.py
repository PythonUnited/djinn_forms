from django.forms.widgets import Widget
from django.utils.safestring import mark_safe
from django.template.loader import render_to_string
from django.core.urlresolvers import reverse
from djinn_contenttypes.utils import urn_to_object, object_to_urn


TPL = 'djinn_forms/snippets/relatewidget.html'


class RelateWidget(Widget):

    """ Widget for handling relations to other content.
    The following extra attributes are supported:
     * content_types Allowed content types for this relation
     * relation_type Relation type to use for creating the actual relation
     * src_obj Source object for relation
    """

    def __init__(self, src_obj, relation_type, content_types=None, attrs=None):

        super(RelateWidget, self).__init__(attrs=attrs)
        self.relation_type = relation_type
        self.src_obj = src_obj
        self.content_types = content_types or []

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
            ",".join(self.content_types),
            self.attrs.get("searchfield", "title")
            )

        value = [{'label': rel.title, 'value': object_to_urn(rel)} for rel in \
                     self.src_obj.get_related(self.relation_type)]

        context = {'name': name,
                   'label': self.label,
                   'hint': self.attrs.get("hint", ""),
                   'value': value,
                   'search_minlength': self.attrs.get("search_minlength", 2),
                   'search_url': url
                   }

        context.update(self.__dict__)

        context['restrict_content_types'] = \
            ",".join(context.get('content_types', []))

        html = render_to_string(TPL, context)

        return mark_safe(u"".join(html))

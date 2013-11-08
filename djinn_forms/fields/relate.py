from django.forms.fields import Field
from djinn_forms.widgets.relate import RelateWidget
from djinn_contenttypes.utils import object_to_urn


class RelateField(Field):

    """ Field for relations, based on """

    widget = RelateWidget

    def __init__(self, relation_type, content_types, *args, **kwargs):

        self.relation_type = relation_type
        self.content_types = content_types
        self.instance = None

        super(RelateField, self).__init__(*args, **kwargs)

    def save_relations(self, obj, data):

        """ Save relations given in the data, by keys 'rm' and 'add' """

        # Unrelate
        for tgt in data.get('rm', []):
            obj.rm_relation(self.relation_type, tgt)

        # Relate
        for tgt in data.get('add', []):
            obj.add_relation(self.relation_type, tgt)

    def widget_attrs(self, widget):

        """Renders this field as an HTML widget."""

        attrs = super(RelateField, self).widget_attrs(widget)

        attrs.update({'content_types': self.content_types})

        return attrs

    def prepare_value(self, data):

        """ Return relations for this field. If data is empty,
        we simply get the related objects for the given type.
        If data['rm'] has values, filter those out of the result.
        If data['add'] has values, add those to the result
        """

        relations = self.instance.get_related(self.relation_type)

        relations = filter(lambda x: x not in data['rm'], relations)

        relations += data['add']

        return [{'label': rel.title, 'value': object_to_urn(rel)} for rel in \
                    relations]

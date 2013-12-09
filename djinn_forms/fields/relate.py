from django.forms.fields import Field
from djinn_forms.widgets.relate import RelateWidget
from djinn_contenttypes.utils import object_to_urn


class UpdateRelations(object):

    def __init__(self, instance, rms, adds, relation_type):
        self.instance = instance
        self.rms = rms
        self.adds = adds
        self.relation_type = relation_type

    def update(self):

        # Unrelate
        for tgt in self.rms:

            #if callable(self.relation_type):
            #    rtype = self.relation_type(tgt)
            #else:
            rtype = self.relation_type

            self.instance.rm_relation(rtype, tgt)

        # Relate
        for tgt in self.adds:

            #if callable(self.relation_type):
            #    rtype = self.relation_type(tgt)
            #else:
            rtype = self.relation_type

            self.instance.add_relation(rtype, tgt)


class RelateField(Field):

    """ Field for relations, based on """

    widget = RelateWidget
    updater = UpdateRelations

    def __init__(self, relation_type, content_types, *args, **kwargs):

        self.relation_type = relation_type
        self.content_types = content_types
        self.instance = None

        super(RelateField, self).__init__(*args, **kwargs)

    def save_relations(self, obj, data, commit):

        """ Save relations given in the data, by keys 'rm' and 'add' """

        relation_updater = self.updater(
            obj, data.get('rm', []), data.get('add', []), self.relation_type)

        if commit:
            relation_updater.update()

        else:

            # append the updater instance to the object. Note that it's a list
            # since there can be more than one relation field per instance
            if not hasattr(obj, '_relation_updater'):
                obj._relation_updater = []
            obj._relation_updater.append(relation_updater)

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

        if callable(self.relation_type):
            rtype = self.relation_type(tgt)
        else:
            rtype = self.relation_type

        relations = self.instance.get_related(self.relation_type)

        try:
            relations = filter(lambda x: x not in data['rm'], relations)
        except:
            pass

        try:
            relations += data['add']
        except:
            pass

        return [{'label': rel.title, 'value': object_to_urn(rel)} for rel in
                relations]

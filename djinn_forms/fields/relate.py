from django.forms.fields import Field
from djinn_forms.widgets.relate import RelateWidget
from djinn_contenttypes.utils import get_object_by_ctype_id


class RelateField(Field):

    """ Field for relations, based on """

    widget = RelateWidget

    def save_relations(self, obj, data):

        """ Save relations given in the data, by keys 'rm' and 'add' """

        # Unrelate
        for ctype, cid in data.get('rm', []):
            tgt = get_object_by_ctype_id(ctype, cid)

            obj.rm_relation(self.widget.relation_type, tgt)

        # Relate
        for ctype, cid in data.get('add', []):
            tgt = get_object_by_ctype_id(ctype, cid)

            obj.add_relation(self.widget.relation_type, tgt)

    def widget_attrs(self, widget):
    
        """Renders this field as an HTML widget."""

        widget.label = self.label
        widget.help_text = getattr(self, "help_text", "")

        return {}

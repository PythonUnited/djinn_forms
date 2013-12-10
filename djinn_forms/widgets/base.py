from django.forms.widgets import Widget
from django.utils.safestring import mark_safe
from django.template.loader import render_to_string


class BaseWidget(Widget):

    defaults = {}

    def __init__(self, attrs=None):

        _attrs = self.defaults.copy()

        if attrs:
            _attrs.update(attrs)

        super(BaseWidget, self).__init__(attrs=_attrs)

    @property
    def template_name(self):

        raise NotImplementedError

    def build_attrs(self, extra_attrs=None, **kwargs):

        return super(BaseWidget, self).build_attrs(
            extra_attrs=extra_attrs, **kwargs)

    """ Base widget that renders a template """

    def render(self, name, value, attrs=None):

        final_attrs = self.build_attrs(attrs, name=name, value=value)

        html = render_to_string(self.template_name, final_attrs)

        return mark_safe(u"".join(html))

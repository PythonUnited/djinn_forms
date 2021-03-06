from .base import BaseWidget
from datetime import datetime
from django.forms import Media


class DateTimeWidget(BaseWidget):

    """
    Widget that renders the datetime as two separate boxes, using jQuery
    to bind the appropriate client side widgets.
    The following attrs are supported:

     * date_format Defaults to dd-mm-YYYY
     * time_format Defaults to hh:mm
    """

    def _media(self):

        """ Add JS for TinyMCE """

        return Media(
            js=('js/djinn_forms_datetimedirect.js', ),
        )

    def _template_name(self):

        if self.attrs.get("direct"):
            Templ = 'djinn_forms/snippets/datetimedirectwidget.html'
        else:
            Templ = 'djinn_forms/snippets/datetimewidget.html'

        return Templ

    media = property(_media)
    template_name = property(_template_name)
    defaults = {'date_format': '%d-%m-%Y', 'time_format': '%H:%M'}

    def build_attrs(self, attrs=None, extra_attrs=None, **kwargs):

        final_attrs = super(DateTimeWidget, self).build_attrs(
            attrs, extra_attrs=extra_attrs, **kwargs)

        the_datetime = kwargs.get('value') or extra_attrs.get('value')

        if final_attrs.get('modal', False):
            # adds a prefix to the date and time inputs for modal form
            # this prevents the datetimepicker from populating the main page's
            # publish_from an publish_to fields
            final_attrs['id_prefix'] = "modal_"
        else:
            final_attrs['id_prefix'] = ""

        if the_datetime:
            if the_datetime == "errorDirect":
               final_attrs['direct'] = ""
               final_attrs['notdirect'] = "checked"
            else:
                final_attrs['date_value'] = \
                    the_datetime.strftime(self.attrs['date_format'])
                final_attrs['time_value'] = \
                    the_datetime.strftime(self.attrs['time_format'])
        else:
            final_attrs['date_value'] = ""
            final_attrs['time_value'] = ""
            final_attrs['direct'] = "checked"
            final_attrs['notdirect'] = ""

        return final_attrs

    def value_from_datadict(self, data, files, name):

        value = None

        if data.get("%s_date" % name):

            value_str = data['%s_date' % name]
            format_str = self.attrs['date_format']

            if data.get("%s_time" % name):

                value_str = "%s %s" % (value_str, data['%s_time' % name])
                format_str = "%s %s" % (format_str, self.attrs['time_format'])

            value = datetime.strptime(value_str, format_str)
        else:
            if name=="publish_from" and data.get("radiodirect") == "NotDirect":
                value="errorDirect"

        return value

    def value_omitted_from_data(self, data, files, name):
        # Fields exist as publish_from_date, publish_from_time,
        # publish_to_date or publish_to_time in the request data
        # of which *_date is mandatory

        name = "%s_date" % name

        if name == 'publish_from_date':
            return False

        return super(DateTimeWidget, self).value_omitted_from_data(
            data, files, name)

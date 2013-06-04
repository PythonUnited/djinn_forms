from django.forms.fields import Field
from djinn_forms.widgets.image import ImageWidget


class ImageField(Field):

    """ Convert given value to image """

    widget = ImageWidget

    def __init__(self, model=None, **kwargs):

        super(ImageField, self).__init__(**kwargs)

        self.model = model

    def to_python(self, value):

        return self.model.objects.get(pk=value).image        

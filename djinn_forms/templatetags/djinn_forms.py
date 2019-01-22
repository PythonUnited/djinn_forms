from djinn_core.utils import urn_to_object
from django.template import Library
from django.template.defaultfilters import stringfilter
from django.conf import settings
import bleach

import sys
if sys.version_info[0] == 3:
    basestring = str

ALLOWED_TAGS = getattr(settings, 'SANITIZER_ALLOWED_TAGS', [])
ALLOWED_ATTRIBUTES = getattr(settings, 'SANITIZER_ALLOWED_ATTRIBUTES', [])
ALLOWED_STYLES = getattr(settings, 'SANITIZER_ALLOWED_STYLES', [])
ALLOWED_PROTOCOLS = getattr(settings, 'SANITIZER_ALLOWED_PROTOCOLS', [])


register = Library()


@register.inclusion_tag('djinn_forms/snippets/link.html')
def link_as_a(link):

    ctx = {}

    _link = link.split("::")[0]

    if _link.startswith("urn"):

        obj = urn_to_object(_link)

        ctx['url'] = obj.get_absolute_url()
        ctx['title'] = obj.title
    else:
        ctx['url'] = ctx['title'] = _link

    ctx['target'] = link.split("::")[1] or ""

    return ctx

@stringfilter
def pg_strip_filter(value):
    '''
    Strips HTML tags from strings according to SANITIZER_ALLOWED_TAGS,
    SANITIZER_ALLOWED_ATTRIBUTES, SANITIZER_ALLOWED_PROTOCOLS and
    SANITIZER_ALLOWED_STYLES variables in
    settings.

    Example usage:

    {% load djinn_forms %}
    {{ post.content|pg_strip_html }}

    '''
    if isinstance(value, basestring):
        value = bleach.clean(value, tags=ALLOWED_TAGS,
                             attributes=ALLOWED_ATTRIBUTES,
                             styles=ALLOWED_STYLES,
                             protocols=ALLOWED_PROTOCOLS,
                             strip=True)
    return value

register.filter('pg_strip_html', pg_strip_filter)

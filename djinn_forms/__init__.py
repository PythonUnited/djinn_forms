
def get_js():

    return ["djinn_forms.js", "djinn_forms_relate.js"]


def get_css():

    return ["djinn_forms.css"]


def get_urls():

    from .urls import urlpatterns

    return urlpatterns

import json
from django.conf import settings
from django.http import HttpResponse
from django.views.generic import View
from haystack.query import SearchQuerySet
from haystack.inputs import Raw
from djinn_core.utils import object_to_urn
from djinn_contenttypes.registry import CTRegistry


def map_swappable_ct(ct_name):

    """ Is the model swappable? If so, what is the underlying model """

    result = ct_name

    try:
        swapped_ct_name = CTRegistry.get(ct_name)['class']._meta.swappable

        if swapped_ct_name:
            result = getattr(settings, swapped_ct_name, ct_name).lower()
    except:
        pass

    return result


class RelateSearch(View):

    """ Find related stuff, using autocomplete """

    def get(self, request, term=None):

        term = term or request.GET.get('term', '')

        if not term:
            return HttpResponse(
                json.dumps([]),
                content_type='application/json')

        search_field = "%s__contains" % request.GET.get("searchfield",
                                                        "title")

        ct_parameter = request.GET.get("ct_searchfield", "meta_ct")

        ct_search_field = "%s__in" % ct_parameter

        content_types = request.GET.get('content_type', '').split(",")

        # MJB map
        # content_types = map(map_swappable_ct, content_types)
        content_types = [map_swappable_ct(ctn) for ctn in content_types]

        _filter = {search_field: Raw("*%s*" % term)}

        if content_types:
            _filter[ct_search_field] = content_types

        parentusergroup = request.GET.get("parentusergroup", None)
        if parentusergroup and parentusergroup != '-1':
            _filter['parentusergroup'] = parentusergroup

        sqs = SearchQuerySet().filter(**_filter)

        results = []

        for res in [res for res in sqs if res.object]:
            results.append({"label": str(res.object),
                            "value": object_to_urn(res.object)
                            })

        if len(results) == 0:
            results.append({"label": "Geen resultaat gevonden",
                            "value": ''})

        return HttpResponse(json.dumps(results), content_type='application/json')

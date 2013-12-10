import json
from django.http import HttpResponse
from django.views.generic import View
from haystack.query import SearchQuerySet
from haystack.inputs import Raw
from djinn_contenttypes.utils import object_to_urn


class RelateSearch(View):

    """ Find related stuff, using autocomplete """

    def get(self, request, term=None):

        term = term or request.GET.get('term', '')

        if not term:
            return HttpResponse(
                json.dumps([]),
                mimetype='application/json')

        search_field = "%s__contains" % request.GET.get("searchfield",
                                                        "title")

        ct_search_field = "%s__in" % request.GET.get("ct_searchfield",
                                                     "meta_ct")

        content_types = request.GET.get('content_types', '').split(",")

        _filter = {search_field: Raw("*%s*" % term)}

        if content_types:
            _filter[ct_search_field] = content_types

        sqs = SearchQuerySet().filter(**_filter)

        results = []

        for res in [res for res in sqs if res.object]:
            results.append({"label": unicode(res.object),
                            "value": object_to_urn(res.object)
                            })

        return HttpResponse(json.dumps(results), mimetype='application/json')

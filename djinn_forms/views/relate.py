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

        _filter = {search_field: Raw("*%s*" % term)}

        sqs = SearchQuerySet().filter(**_filter)

        sqs = sqs.filter(
            meta_ct__in=request.GET.get('content_types', '').split(","))

        results = []

        for res in [res for res in sqs if res.object]:
            results.append({"label": unicode(res.object),
                            "value": object_to_urn(res.object)
                            })

        return HttpResponse(json.dumps(results), mimetype='application/json')

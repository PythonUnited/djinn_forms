import json
from django.http import HttpResponse
from django.views.generic import View
from haystack.query import SearchQuerySet
from haystack.inputs import Raw
from djinn_contenttypes.registry import CTRegistry
from djinn_contenttypes.utils import object_to_urn


class RelateSearch(View):

    """ Find related stuff, using autocomplete """

    def get(self, request, term=None):

        term = term or request.GET.get('term', '')

        if not term:
            return HttpResponse(
                json.dumps([]),
                mimetype='application/json')

        _filter = {
            request.GET.get('searchfield'): Raw("*%s*" %term)
            }

        sqs = SearchQuerySet().filter(**_filter)

        for ct in request.GET.get("content_types", "").split(","):

            clazz = CTRegistry.get(ct)['class']
            sqs = sqs.models(clazz)

        results = []

        for res in sqs:
            results.append({"label": res.title,
                            "value": object_to_urn(res.object)
                            })

        return HttpResponse(json.dumps(results), mimetype='application/json')

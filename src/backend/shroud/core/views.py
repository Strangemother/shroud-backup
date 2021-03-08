from django.shortcuts import render

# Create your views here.
"""
1. Recv JSON
2. Store results
    diff and remove unselected
3. Return objects as JSON
"""

from django.views.generic import TemplateView
from django.http import JsonResponse
from django.views.generic import DetailView

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect, csrf_exempt
import json


def bulk_replace(M, r):
    M.objects.all().delete()
    M.objects.bulk_create(r)


def json_to_models(body, M, keys):
    print('Post')

    try:
        data = json.loads(body)
    except Exception as exc:
        import pdb; pdb.set_trace()  # breakpoint 5a32b9f1x //

    r= ()
    # [x.name for x in M._meta.get_fields()]

    for new_item in data:
        m = M(**{x:new_item[x] for x in keys})
        r += (m,)

    return r


def as_json(_models, keys):
    res = ()

    for item in _models:
        o = {}
        for k in keys:
            o[k] = getattr(item,k)
        res += (o,)
    return res



class JsonBaseView(TemplateView):
    # def get_queryset(self):
    template_name = 'dummy.html'

    def get(self, request, *args, **kwargs):
        content = self.get_content(**kwargs)
        data = self.get_context_data(content=content)

        if 'view' in data:
            data.pop('view')
        return JsonResponse(data)
        # return self.render_to_response(data)
        #

    def get_context_data(self, **kwargs):
        """Insert the single object into the context dict."""
        return super().get_context_data(**kwargs)

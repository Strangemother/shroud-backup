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

from . import models
from core.views import *

@method_decorator(csrf_exempt, name='dispatch')
class DrivesPost(JsonBaseView):

    def post(self, request, *args, **kwargs):
        # content = self.get_content(**kwargs)
        print('Post')

        r= ()
        M = models.Drive
        # [x.name for x in M._meta.get_fields()]
        keys = (
            'caption', 'compressed',
            'name', # 'provider_name',
            'size', 'system_name',
            'volume_name', )

        r = json_to_models(request.body, M, keys)
        bulk_replace(M, r)
        rd = as_json(r, keys)
        return JsonResponse({'drives': rd})

    def get_content(self, **kwargs):
        content = { 'd': [1,2,3,4,5]}
        return content

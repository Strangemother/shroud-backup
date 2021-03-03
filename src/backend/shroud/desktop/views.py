from django.shortcuts import render

from django.views.generic import TemplateView
from django.http import JsonResponse
from django.views.generic import DetailView


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


class Example(JsonBaseView):
    def get_content(self, **kwargs):
        content = { 'd': [1,2,3,4,5]}
        return content


class WelcomePage(TemplateView):
    template_name = 'desktop/welcome.html'

from core.views import JsonBaseView, TemplateView

class Example(JsonBaseView):
    def get_content(self, **kwargs):
        content = { 'd': [1,2,3,4,5]}
        return content


class WelcomePage(TemplateView):
    template_name = 'desktop/welcome.html'


class ConfiguredPage(TemplateView):
    template_name = 'desktop/configured.html'


class ExplorerView(TemplateView):
    template_name = 'desktop/explorer.html'

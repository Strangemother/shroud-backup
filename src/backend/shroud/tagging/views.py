from . import models
from core.views import *

import string, random
# printing letters
letters = string.ascii_letters

def random_string():
    return ''.join(random.choice(letters) for i in range(10))


@method_decorator(csrf_exempt, name='dispatch')
class TagPost(JsonBaseView):

    def post(self, request, *args, **kwargs):
        # content = self.get_content(**kwargs)

        content = json.loads(request.body)
        path = content['path']
        entry, cr = models.Entry.objects.get_or_create(filepath=path)

        M = models.Tag
        bulk_id = random_string()
        tags = tuple(M(name=x, bulk_id=bulk_id) for x in content['tags'])
        bt = M.objects.bulk_create(tags, ignore_conflicts=False)

        tags = entry.tags.add(*M.objects.filter(bulk_id=bulk_id))

        return JsonResponse({ 'is_new': cr })

    def get_content(self, **kwargs):
        content = { 'd': [1,2,3,4,5]}
        return content

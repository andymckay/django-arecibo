from django.conf import settings
from django.http import Http404
from wrapper import post
from tasks import post as delayed_post

def arecibo_post(method, request, exception):
    if getattr(settings, 'ARECIBO_SERVER_URL', ''):
        if isinstance(exception, Http404):
            method(request, 404)
        else:
            method(request, 500)

class AreciboMiddleware(object):

    def process_exception(self, request, exception):
        return arecibo_post(post, request, exception)

class AreciboMiddlewareCelery(object):

    def process_exception(self, request, exception):
        return arecibo_post(delayed_post, request, exception)

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.http import Http404
from django_arecibo.wrapper import post

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

    def __init__(self):
        '''
        Unlike the process_* methods which get called once per request,
        __init__ gets called only once, when the Web server starts up.
        
        (https://docs.djangoproject.com/en/dev/topics/http/middleware/#s-init)
        '''
        try:
            from django_arecibo.tasks import post as delayed_post
        except ImportError, e:
            if str(e) == 'No module named celery.decorators':
                raise ImproperlyConfigured('Cannot use AreciboMiddlewareCelery\
                    if Celery is not installed.')
            raise e

    def process_exception(self, request, exception):
        return arecibo_post(delayed_post, request, exception)

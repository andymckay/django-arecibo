from celery.decorators import task
from django_arecibo.wrapper import DjangoPost

@task
def delayed_send(obj):
    obj.send()

def post(request, status, **kw):
    obj = DjangoPost(request, status, **kw)
    if obj and hasattr(obj, 'data'):
        delayed_send.delay(obj)
        return obj.data.get("uid")

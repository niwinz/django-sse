# -*- coding: utf-8 -*-

from django.http import HttpResponse
from .response import Response
import functools
import types

class Sse(object):
    def __init__(self, retry=None):
        self.retry = retry

    def __call__(self, viewfunc):
        response = Response()
        if self.retry is not None:
            response.set_retry(self.retry)

        def _get_last_id(request):
            if 'HTTP_LAST_EVENT_ID' in request.META:
                return request.META['HTTP_LAST_EVENT_ID']
            return None

        @functools.wraps(viewfunc)
        def _inner(self, request, *args, **kwargs):
            self.sse = response
            self.sse._last_id = _get_last_id(request)
            viewfunc(self, request, *args, **kwargs)
            return HttpResponse(response.get_unicode(),
                mimetype='text/event-stream')

        return _inner


def is_sse_method(retry=2000):
    if isinstance(retry, (types.FunctionType, types.MethodType)):
        sseinstance = Sse()(retry)
    else:
        sseinstance = Sse(retry)
    return sseinstance

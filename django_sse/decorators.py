# -*- coding: utf-8 -*-

from django.http import HttpResponse
from .response import Response, DEFAULT_RETRY_TIMEOUT
from . import __version__ as v
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
            http_response = HttpResponse(response.get_unicode(),
                mimetype='text/event-stream')
            http_response['Cache-Control'] = 'no-cache'
            http_response['Software'] = 'django-sse {0[0]}.{0[1]}'.format(v)
            return http_response

        return _inner


def is_sse_method(retry=DEFAULT_RETRY_TIMEOUT):
    """
    Declare class view method as sse method.
    """

    if isinstance(retry, (types.FunctionType, types.MethodType)):
        return Sse()(retry)
    
    return Sse(retry)

# -*- coding: utf-8 -*-

from django.http import HttpResponse
from .response import Response, DEFAULT_RETRY_TIMEOUT, DEFAULT_SLEEP
from . import __version__ as v

import functools
import types
import time

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


class StreamSse(object):
    def __init__(self, retry=DEFAULT_RETRY_TIMEOUT, sleep=1):
        self.retry = retry
        self.sleep = sleep

    def __call__(self, viewfunc):
        response = Response()

        if self.retry is not None:
            response.set_retry(self.retry)
        
        def _get_last_id(request):
            if 'HTTP_LAST_EVENT_ID' in request.META:
                return request.META['HTTP_LAST_EVENT_ID']
            return None

        sleep_time = self.sleep

        @functools.wraps(viewfunc)
        def _inner(self, request, *args, **kwargs):
            self.sse = response
            self.sse._last_id = _get_last_id(request)
            
            def gen():
                while 1:
                    viewfunc(self, request, *args, **kwargs)
                    yield self.sse.get_unicode()
                    time.sleep(sleep_time)

            http_response = HttpResponse(gen(), mimetype='text/event-stream')
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


def is_stream_sse_method(retry=DEFAULT_RETRY_TIMEOUT, sleep=DEFAULT_SLEEP):
    """
    Declare class view method as sse stream method.
    """
    return StreamSse(retry=retry, sleep=sleep)

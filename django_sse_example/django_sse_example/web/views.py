# Create your views here.

from django.shortcuts import render_to_response
from django.views.generic import View
from django.template import RequestContext
from django.utils.timezone import now

class Home1(View):
    def get(self, request):
        return render_to_response('home.html', {},
            context_instance=RequestContext(request))


class Home2(View):
    def get(self, request):
        return render_to_response('home2.html', {},
            context_instance=RequestContext(request))


from django_sse.decorators import is_sse_method, is_stream_sse_method

class MyEvents(View):
    @is_sse_method
    def get(self, request):
        now_date = unicode(now())

        self.sse.add_message('message', 'Hello World')
        self.sse.event_date(text=now_date)


class MyEvents2(View):
    @is_stream_sse_method(sleep=1)
    def get(self, request):
        now_date = unicode(now())
        self.sse.add_message('message', 'Hello World')
        self.sse.event_date(text=now_date)

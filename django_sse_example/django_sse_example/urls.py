from django.conf.urls import patterns, include, url

from .web.views import *

urlpatterns = patterns('',
    url(r'^$', Home.as_view(), name='home'),
    url(r'^events/$', MyEvents.as_view(), name='events'),
)

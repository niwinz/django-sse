from django.conf.urls import patterns, include, url

from .web.views import *

urlpatterns = patterns('',
    url(r'^home1/$', Home1.as_view(), name='home1'),
    url(r'^home2/$', Home2.as_view(), name='home2'),

    url(r'^events1/$', MyEvents.as_view(), name='events1'),
    url(r'^events2/$', MyEvents2.as_view(), name='events2'),
)

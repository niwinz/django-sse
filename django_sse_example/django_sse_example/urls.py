from django.conf.urls import patterns, include, url

from .web.views import *
from django_sse.redisqueue import RedisQueueView

urlpatterns = patterns('',
    url(r'^home1/$', Home1.as_view(), name='home1'),
    url(r'^home2/$', Home2.as_view(), name='home2'),

    url(r'^events1/$', MySseEvents.as_view(), name='events1'),
    url(r'^events2/$', RedisQueueView.as_view(), name='events2'),
)

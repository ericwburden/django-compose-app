from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/counter/(?P<counter_name>\w+)/$', consumers.CounterConsumer),
]
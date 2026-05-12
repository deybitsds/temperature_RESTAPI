from django.urls import re_path
from temperature.consumers import TemperatureConsumer

websocket_urlpatterns = [
    re_path(r'ws/temperature/$', TemperatureConsumer.as_asgi()),
]

from django.urls import re_path

from .consumers import OnlineStatusConsumer, PhoneConsumer
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/online/$', OnlineStatusConsumer.as_asgi()),
    re_path(r'ws/phones/$', PhoneConsumer.as_asgi()),
    path('ws/operations/', consumers.OperationConsumer.as_asgi()),

]

application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    ),
})

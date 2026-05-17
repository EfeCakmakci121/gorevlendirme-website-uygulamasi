from django.urls import re_path
from . import consumers
from .schemas.mutation import schema
from strawberry.channels.handlers.ws_handler import GraphQLWSConsumer

websocket_urlpatterns = [
    # re_path(r"^ws/gorev/$",consumers.GorevNotificationConsumer.as_asgi()),
    # re_path(r"graphql/?$", GraphQLWSConsumer.as_asgi(schema=schema)),
    re_path(r'ws/notifications/$', consumers.NotificationConsumer.as_asgi()),
]
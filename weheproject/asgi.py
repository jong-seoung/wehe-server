"""
ASGI config for weheproject project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

from channels.auth import AuthMiddlewareStack
from django.urls import path, re_path
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
import django_eventstream


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "weheproject.settings")

django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter(
    {
        'http': URLRouter([
            path('events/<user_id>/', AuthMiddlewareStack(
                URLRouter(django_eventstream.routing.urlpatterns)
            ), {'format-channels': ['user-{user_id}']}),
            re_path(r'', get_asgi_application()),
        ]),
    }
)
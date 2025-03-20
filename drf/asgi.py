"""
ASGI config for drf project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
import api.routing
from django.urls import path
from api.consumers import DatosConsummer



os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'drf.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": URLRouter(
        [path("ws/datos/",DatosConsummer.as_asgi()),
         ]
    ),
})
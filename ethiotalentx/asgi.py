"""
ASGI config for ethiotalentx project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ethiotalentx.settings')
os.environ.setdefault("DJANGO_CONFIGURATION", "Prod")

from channels.routing import ProtocolTypeRouter , URLRouter
from chat import routing
from channels.auth import AuthMiddlewareStack



application = ProtocolTypeRouter(
    {
        "http" : get_asgi_application() , 
        "websocket" : AuthMiddlewareStack(
            URLRouter(
                routing.websocket_urlpatterns
            )    
        )
    }
)

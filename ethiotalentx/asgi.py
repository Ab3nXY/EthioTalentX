"""
ASGI config for ethiotalentx project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

"""
ASGI config for ethiotalentx project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os

from channels.auth import AuthMiddlewareStack  # Optional for authentication
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ethiotalentx.settings')

# Initialize Django ASGI application early to ensure AppRegistry is populated
django_asgi_app = get_asgi_application()

from chat import routing  # Assuming your consumers are defined in chat.routing

application = ProtocolTypeRouter({
    "http": django_asgi_app,

    # WebSocket chat handler with security considerations
    "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack(  # Optional for authentication
            URLRouter(
                routing.websocket_urlpatterns
            )
        )
    ),
})


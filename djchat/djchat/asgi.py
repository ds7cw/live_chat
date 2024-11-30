"""
ASGI config for djchat project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os

from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djchat.settings')
django_application = get_asgi_application()

from . import urls # placement after .settings is intentional


# application = get_asgi_application()
application = ProtocolTypeRouter(
    {
        'http': get_asgi_application(),
        'websocket': URLRouter(urls.websocket_urlpatterns),
    }
)

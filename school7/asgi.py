import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter,URLRouter
import app.routing
from channels.auth import AuthMiddleware

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school6.settings')
application=ProtocolTypeRouter({
    'http':get_asgi_application(),
    'websocket':AuthMiddleware(
        URLRouter(
        app.routing.websocket_urlpatterns
        )
    )
    })
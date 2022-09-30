from django.urls import path
from . import consumers

websocket_urlpatterns=[
    path('ws/jwc/<str:groupkaname>/',consumers.MyJsonWebSocketCunsumer.as_asgi()),
    path('ws/ajwc/',consumers.MyasyncJsonWebSocketCunsumer.as_asgi()),
]
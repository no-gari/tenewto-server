from django.urls import path
from api.chat.consumers import ChatConsumer

websocket_urlpatterns = [
    path('ws/chat/<str:chat_id>/', ChatConsumer.as_asgi()),
]

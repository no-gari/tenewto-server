from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from django.urls import path

# 챗 라우팅과 미들웨어 임포트
import api.chat.routing
from api.chat.middleware import TokenAuthMiddlewareStack

# ASGI 애플리케이션 정의
application = ProtocolTypeRouter({
    # HTTP 요청 처리 (Django의 기본 WSGI 애플리케이션)
    'http': get_asgi_application(),

    # WebSocket 연결 처리
    'websocket': TokenAuthMiddlewareStack(
        URLRouter([
            # 챗 관련 웹소켓 라우트들
            *api.chat.routing.websocket_urlpatterns,
            # 필요한 경우 다른 웹소켓 라우트들도 추가 가능
            # path('ws/notifications/', NotificationConsumer.as_asgi()),
        ])
    ),
})

# 개발 환경에서 디버깅을 위한 설정
import os

if os.environ.get('DEBUG') == 'True':
    import logging

    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger('channels')
    logger.setLevel(logging.DEBUG)
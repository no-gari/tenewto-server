from urllib.parse import urlsplit, parse_qsl

from channels.auth import AuthMiddleware
from channels.db import database_sync_to_async
from channels.sessions import SessionMiddleware, CookieMiddleware
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.tokens import AccessToken

from api.user.models import User


@database_sync_to_async
def get_user(scope):
    query_string = scope['query_string'].decode('utf-8')
    query_string = dict(parse_qsl(urlsplit(query_string).path))
    access = query_string.get('access')
    if access:
        access_token = AccessToken(access)
        try:
            user = User.objects.get(pk=access_token.payload['user_id'])
            return user
        except User.DoesNotExist:
            return AnonymousUser()
    else:
        return AnonymousUser()


class TokenAuthMiddleware(AuthMiddleware):
    async def resolve_scope(self, scope):
        scope['user']._wrapped = await get_user(scope)


TokenAuthMiddlewareStack = lambda inner: CookieMiddleware(
    SessionMiddleware(TokenAuthMiddleware(inner))
)

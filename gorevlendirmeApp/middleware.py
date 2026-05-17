from urllib.parse import parse_qs
from channels.middleware import BaseMiddleware
from django.contrib.auth.models import AnonymousUser
from knox.auth import TokenAuthentication
from channels.db import database_sync_to_async # Bura değişti

class TokenAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        query_string = scope.get("query_string", b"").decode()
        query_params = parse_qs(query_string)
        token = query_params.get("token", [None])[0]

        scope["user"] = AnonymousUser()

        if token:
            user = await self.get_user(token)
            if user:
                scope["user"] = user

        return await super().__call__(scope, receive, send)

    @database_sync_to_async
    def get_user(self, token):
        try:
            user, auth_token = TokenAuthentication().authenticate_credentials(token.encode())
            return user
        except Exception as e:
            print(f"WebSocket Auth Hatası: {e}")
            return None
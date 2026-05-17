# consumers.py veya uygun bir yerde
from strawberry.asgi import GraphQL
from knox.auth import TokenAuthentication
from django.contrib.auth.models import AnonymousUser

class CustomGraphQLView(GraphQL):
    async def get_context(self, request, response):
        token_auth = TokenAuthentication()
        user = AnonymousUser()

        auth_header = request.headers.get("authorization")
        if auth_header and auth_header.startswith("Token "):
            token = auth_header.split("Token ")[1]
            try:
                user_auth_tuple = token_auth.authenticate_credentials(token.encode())
                user = user_auth_tuple[0]
            except Exception:
                pass

        # context içine istediğini koyabilirsin
        return {"request": request, "user": user}

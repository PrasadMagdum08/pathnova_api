import jwt
from django.conf import settings
from rest_framework import authentication, exceptions
from django.contrib.auth.models import AnonymousUser

class NodeJWTAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return None  # no token provided

        token = auth_header.split(" ")[1]
        try:
            payload = jwt.decode(token, settings.NODE_JWT_SECRET, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed("Token expired")
        except jwt.InvalidTokenError:
            raise exceptions.AuthenticationFailed("Invalid token")

        # Since the user is from MongoDB/Node and not Django's User model:
        user = AnonymousUser()
        user.email = payload.get("email", None)
        user.id = payload.get("id", None)
        user.role = payload.get("role", None)

        return (user, token)

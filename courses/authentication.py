# authentication.py

from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
import jwt
import os

SECRET_KEY = os.environ.get("JWT_SECRET", "supersecretjwtkey")  # must match Node's .env

class NodeJWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth = request.headers.get("Authorization", "")
        if not auth.startswith("Bearer "):
            raise AuthenticationFailed("Token missing")

        token = auth.split(" ")[1]
        try:
            decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Token expired")
        except jwt.InvalidTokenError:
            raise AuthenticationFailed("Invalid token")

        email = decoded.get("email")
        if not email:
            raise AuthenticationFailed("Token missing email")

        user = type("User", (), {"email": email})
        return (user, token)

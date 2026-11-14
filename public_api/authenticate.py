"""Authenticate requests using the JWT issued by the auth service."""
import os

import jwt
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from rest_framework import authentication, exceptions


class CustomAuthentication(authentication.BaseAuthentication):
    def authenticate_header(self, request):
        return 'Bearer'

    def authenticate(self, request):
        header = authentication.get_authorization_header(request).split()
        if not header:
            return None
        if len(header) != 2 or header[0].lower() != b'bearer':
            raise exceptions.AuthenticationFailed('Invalid Authorization header')

        secret = os.getenv('JWT_SECRET')
        if not secret:
            raise exceptions.APIException('Token verification unavailable')

        try:
            claims = jwt.decode(header[1], secret, algorithms=['HS256'])
            user_id = claims.get('id')
            username = claims.get('username')
            if not isinstance(username, str) or not username:
                raise ValueError('Invalid username')
            if isinstance(user_id, bool) or not isinstance(user_id, (int, str)):
                raise ValueError('Invalid user ID')
            user_id = int(user_id)
            if not 0 < user_id <= 2**63 - 1:
                raise ValueError('Invalid user ID')
        except (jwt.InvalidTokenError, ValueError) as exc:
            raise exceptions.AuthenticationFailed('Invalid or expired token') from exc

        user_model = get_user_model()
        try:
            user = user_model.objects.get(pk=user_id, username=username)
        except (user_model.DoesNotExist, ValidationError) as exc:
            raise exceptions.AuthenticationFailed('Invalid account') from exc

        # The current signup service creates members with is_active=False.
        return user, claims

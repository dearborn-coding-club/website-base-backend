"""Custom authentication class for the API."""
import os
from rest_framework import authentication
from rest_framework import exceptions
import jwt


class CustomAuthentication(authentication.BaseAuthentication):
    """
    Custom authentication class for the API.
    """
    public_endpoints = [
        'profile/'
    ]

    def authenticate(self, request):
        """
        Authenticate the user using JWT.
        """
        auth_header = request.META.get('HTTP_AUTHORIZATION')

        if request.path in self.public_endpoints:
            return (None, None)

        try:
            jwt_secret = os.environ['JWT_SECRET']
        except KeyError as exc:
            raise exceptions.AuthenticationFailed('JWT_SECRET not set', exc)

        if not auth_header or not auth_header.startswith('Bearer '):
            # This doesn't seem to hit the latter half of the if statement
            # Even when the Bearer token is missing.
            raise exceptions.AuthenticationFailed('Authentication failed, no auth header')
        token = auth_header.split(' ')[1]

        if not token:
            raise exceptions.AuthenticationFailed('Authentication failed, no token')

        try:
            jwt.decode(token, jwt_secret, algorithms=['HS256'])
        except jwt.ExpiredSignatureError as e:
            raise exceptions.AuthenticationFailed('Token has expired' + e)
        except jwt.InvalidTokenError as e:
            # Note: If you pass the iat field, it must be a valid timestamp (not too far in the future,
            # not too far in the past. If you don't pass it, it will be ignored.
            # If the above happens, it throws an `ImmatureSignatureError` exception.
            raise exceptions.AuthenticationFailed('Invalid token' + e)
        except jwt.InvalidSignatureError as e:
            raise exceptions.AuthenticationFailed('Invalid signature' + e)
        except Exception as e:
            raise exceptions.AuthenticationFailed('Authentication' + e)
        return (token, None)


class CustomUser:
    """
    Custom user class for the API.
    """
    def __init__(self, user_id):
        self.id = user_id

    @property
    def is_authenticated(self):
        """
        Returns True if the user is authenticated.
        """
        return True

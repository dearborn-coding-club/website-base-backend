"""
Views for API resources that don't require the django rest framework.
"""
from functools import wraps
from django.http import HttpResponse, HttpRequest, JsonResponse
import requests
import os
import jwt

# python3 -m pip install types-requests ## install stubs for type hinting


def authentication_required(view_func):
    """
      Decorator to check if the user is authenticated.
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        # Example: Check if the user is authenticated
        if not request.user.is_authenticated:
            return JsonResponse({"error": "Authentication required"}, status=401)
        
        # If authenticated, proceed to the view
        return view_func(request, *args, **kwargs)
    return _wrapped_view


def no_authentication_required(view_func):
    """
    Decorator to explicitly allow access without authentication.
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        # No authentication checks, just call the view
        return view_func(request, *args, **kwargs)
    return _wrapped_view


@authentication_required
def notes_view(_: HttpRequest) -> JsonResponse:
    data = {
        "message": "Welcome to the meetup page!",
        "status": "success"
    }
    return JsonResponse(data)


def leetcode_view(_: HttpRequest) -> JsonResponse:
    url = "https://leetcode.com/graphql"
    global_data = """
    query userSessionProgress($username: String!) {
  allQuestionsCount {
    difficulty
    count
  }
  matchedUser(username: $username) {
    submitStats {
      acSubmissionNum {
        difficulty
        count
        submissions
      }
      totalSubmissionNum {
        difficulty
        count
        submissions
      }
    }
  }
}

"""
    response = requests.get(url=url, json={"query": global_data, "variables": {"username": "MgenGlder23"}, "operationName": "userSessionProgress"}, timeout=10)
    return JsonResponse(response.json())


@no_authentication_required
def me_view(req: HttpRequest) -> JsonResponse | HttpResponse:
    """
    View for the /me endpoint. It reads the Authorization header and checks if the JWT token is valid.
    """
    try:
        jwt_secret = os.environ['JWT_SECRET']
    except KeyError:
        return HttpResponse("JWT_SECRET not set", status=500)

    auth_header = req.META.get("HTTP_AUTHORIZATION")

    if not auth_header or not auth_header.startswith('Bearer '):
        # This doesn't seem to hit the latter half of the if statement
        # Even when the Bearer token is missing.
        return HttpResponse('Authentication failed, no auth header', status=401)
    else:
        token = auth_header.split(' ')[1]
    if not token:
        return HttpResponse('Authentication failed, no token', status=401)

    try:
        decoded_token = jwt.decode(token, jwt_secret, algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        return HttpResponse('Token has expired', status=401)
    except jwt.InvalidTokenError:
        # Note: If you pass the iat field, it must be a valid timestamp (not too far in the future,
        # not too far in the past. If you don't pass it, it will be ignored.
        # If the above happens, it throws an `ImmatureSignatureError` exception.
        return HttpResponse('Invalid token', status=401)
    except jwt.InvalidSignatureError:
        return HttpResponse('Invalid signature', status=401)
    except Exception:
        return HttpResponse('Authentication', status=401)

    return JsonResponse(decoded_token)

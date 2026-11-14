"""
Views for API resources that don't require the django rest framework.
"""
from functools import wraps
from django.http import HttpRequest, JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
import requests

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


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def me_view(request):
    """Return the verified token claims for the requesting account."""
    return Response(request.auth)

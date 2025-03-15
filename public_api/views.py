from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render
import requests


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


def me_view(req: HttpRequest) -> JsonResponse:
    if req.user and hasattr(req.user, 'id'):
        return JsonResponse({"user": req.user.id})

    return JsonResponse({"error": "User not authenticated"}, status=401)

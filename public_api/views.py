from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render


def notes_view(_: HttpRequest) -> JsonResponse:
    data = {
        "message": "Welcome to the meetup page!",
        "status": "success"
    }
    return JsonResponse(data)
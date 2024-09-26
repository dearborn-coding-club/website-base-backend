from django.http import JsonResponse


def meetup_view():
    data = {
        "message": "Welcome to the meetup page!",
        "status": "success"
    }
    return JsonResponse(data)


from django.http import JsonResponse

def meetup_view(request):
    data = {
        "message": "Welcome to the meetup page!",
        "status": "success"
    }
    return JsonResponse(data)
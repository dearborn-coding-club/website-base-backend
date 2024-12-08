from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import NoteViewSet
from .views import NoteSummary

router = DefaultRouter()
router.register(r'v2/notes', NoteViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('v2/notes/summary', NoteSummary),
]

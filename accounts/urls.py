from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProfileViewSet, UserViewSet

router = DefaultRouter()
router.register(r'profile', ProfileViewSet)
router.register(r'user', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

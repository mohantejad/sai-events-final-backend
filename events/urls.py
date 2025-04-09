from django.urls import include, path
from rest_framework.routers import DefaultRouter

from events.views import EventViewSet


router = DefaultRouter()
router.register('events', EventViewSet)

urlpatterns = [
    path('event/', include(router.urls)),
]
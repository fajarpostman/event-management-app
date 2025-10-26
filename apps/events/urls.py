from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import VenueViewSet, EventViewSet, TrackViewSet, SpeakerViewSet, SessionViewSet

router = DefaultRouter()
router.register(r"venues", VenueViewSet, basename="venue")
router.register(r"events", EventViewSet, basename="event")
router.register(r"tracks", TrackViewSet, basename="track")
router.register(r"speakers", SpeakerViewSet, basename="speaker")
router.register(r"sessions", SessionViewSet, basename="session")

urlpatterns = [
    path("", include(router.urls)),
]

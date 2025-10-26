from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.shortcuts import get_object_or_404

from .models import Venue, Event, Track, Speaker, Session
from .serializers import (
    VenueSerializer,
    EventSerializer,
    TrackSerializer,
    SpeakerSerializer,
    SessionSerializer,
)

try:
    from apps.core.permissions import IsOrganizerOrReadOnly
    DEFAULT_WRITE_PERMISSION = IsOrganizerOrReadOnly
except Exception:
    DEFAULT_WRITE_PERMISSION = IsAuthenticatedOrReadOnly


class VenueViewSet(viewsets.ModelViewSet):
    queryset = Venue.objects.all()
    serializer_class = VenueSerializer
    permission_classes = [DEFAULT_WRITE_PERMISSION]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name", "address"]


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.select_related("venue").all().order_by("-start_date")
    serializer_class = EventSerializer
    permission_classes = [DEFAULT_WRITE_PERMISSION]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["title", "slug", "description"]
    ordering_fields = ["start_date", "end_date", "title"]

    # optional: provide a custom action to list sessions for an event (if desired)
    # but we keep routes simple and RESTful (sessions belong to tracks)


class TrackViewSet(viewsets.ModelViewSet):
    queryset = Track.objects.select_related("event").all()
    serializer_class = TrackSerializer
    permission_classes = [DEFAULT_WRITE_PERMISSION]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["title", "description"]


class SpeakerViewSet(viewsets.ModelViewSet):
    queryset = Speaker.objects.all()
    serializer_class = SpeakerSerializer
    permission_classes = [DEFAULT_WRITE_PERMISSION]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name", "bio"]


class SessionViewSet(viewsets.ModelViewSet):
    queryset = Session.objects.select_related("track__event", "speaker").all()
    serializer_class = SessionSerializer
    permission_classes = [DEFAULT_WRITE_PERMISSION]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["title", "description", "room"]

    def get_queryset(self):
        """
        Optionally filter sessions by event via query param ?event=<id>
        or by track via ?track=<id>
        """
        qs = super().get_queryset()
        event_id = self.request.query_params.get("event")
        track_id = self.request.query_params.get("track")
        if track_id:
            qs = qs.filter(track_id=track_id)
        elif event_id:
            qs = qs.filter(track__event_id=event_id)
        return qs

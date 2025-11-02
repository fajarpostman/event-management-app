from rest_framework import serializers
from django.utils import timezone
from .models import Venue, Event, Track, Speaker, Session


class VenueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venue
        fields = ["id", "name", "address", "capacity", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]


class EventSerializer(serializers.ModelSerializer):
    venue = VenueSerializer(read_only=True)
    venue_id = serializers.PrimaryKeyRelatedField(
        queryset=Venue.objects.all(), source="venue", write_only=True
    )
    registration_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Event
        fields = [
            "id",
            "title",
            "slug",
            "description",
            "venue",
            "venue_id",
            "capacity",
            "start_date",
            "end_date",
            "created_at",
            "updated_at",
            "registration_count",
        ]
        read_only_fields = ["id", "created_at", "updated_at", "registration_count"]

    def validate(self, attrs):
        venue = attrs.get("venue") or getattr(self.instance, "venue", None)
        capacity = attrs.get("capacity") or getattr(self.instance, "capacity", None)
        start_date = attrs.get("start_date") or getattr(self.instance, "start_date", None)
        end_date = attrs.get("end_date") or getattr(self.instance, "end_date", None)

        if start_date and end_date and end_date <= start_date:
            raise serializers.ValidationError({"end_date": "end_date must be after start_date"})

        if venue and capacity and capacity > venue.capacity:
            raise serializers.ValidationError({"capacity": "Event capacity cannot exceed venue capacity"})

        return attrs


class TrackSerializer(serializers.ModelSerializer):
    event_id = serializers.PrimaryKeyRelatedField(
        source="event", queryset=Event.objects.all(), write_only=True
    )
    event = EventSerializer(read_only=True)

    class Meta:
        model = Track
        fields = ["id", "title", "description", "event", "event_id", "created_at"]
        read_only_fields = ["id", "created_at"]


class SpeakerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Speaker
        fields = ["id", "name", "bio", "website", "twitter", "user", "created_at"]
        read_only_fields = ["id", "created_at"]


class SessionSerializer(serializers.ModelSerializer):
    track_id = serializers.PrimaryKeyRelatedField(
        source="track", queryset=Track.objects.all(), write_only=True
    )
    track = TrackSerializer(read_only=True)
    speaker = SpeakerSerializer(read_only=True)
    speaker_id = serializers.PrimaryKeyRelatedField(
        source="speaker", queryset=Speaker.objects.all(), write_only=True, required=False, allow_null=True
    )

    class Meta:
        model = Session
        fields = [
            "id",
            "title",
            "description",
            "track",
            "track_id",
            "speaker",
            "speaker_id",
            "start_time",
            "end_time",
            "room",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def validate(self, attrs):
        track = attrs.get("track") or getattr(self.instance, "track", None)
        start_time = attrs.get("start_time") or getattr(self.instance, "start_time", None)
        end_time = attrs.get("end_time") or getattr(self.instance, "end_time", None)

        if start_time and end_time and end_time <= start_time:
            raise serializers.ValidationError({"end_time": "end_time must be after start_time"})

        if track and start_time and end_time:
            qs = Session.objects.filter(track=track).exclude(pk=getattr(self.instance, "pk", None)).filter(
                start_time__lt=end_time,
                end_time__gt=start_time,
            )
            if qs.exists():
                raise serializers.ValidationError("Session overlaps with another session in the same track")

        if track and (start_time or end_time):
            event = track.event
            s = start_time or getattr(self.instance, "start_time", None)
            e = end_time or getattr(self.instance, "end_time", None)
            if s and e and not (event.start_date <= s and e <= event.end_date):
                raise serializers.ValidationError("Session must be within parent event start_date and end_date")

        return attrs

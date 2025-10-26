from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models, transaction
from django.utils import timezone

USER_MODEL = settings.AUTH_USER_MODEL


class Venue(models.Model):
    """
    Venue for events. Has a capacity which is used as a hard upper bound
    for event.capacity validation.
    """
    name = models.CharField(max_length=255)
    address = models.TextField(blank=True)
    capacity = models.PositiveIntegerField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Event(models.Model):
    """
    Event (conference). capacity must be <= venue.capacity.
    """
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    venue = models.ForeignKey(Venue, related_name="events", on_delete=models.PROTECT)
    capacity = models.PositiveIntegerField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-start_date"]
        constraints = [
            models.CheckConstraint(check=models.Q(capacity__gte=1), name="event_capacity_positive"),
            models.CheckConstraint(check=models.Q(end_date__gt=models.F("start_date")), name="event_end_after_start"),
        ]

    def clean(self):
        if self.end_date <= self.start_date:
            raise ValidationError({"end_date": "end_date must be after start_date"})
        if self.capacity < 1:
            raise ValidationError({"capacity": "capacity must be at least 1"})
        if self.venue and self.capacity > self.venue.capacity:
            raise ValidationError({"capacity": "Event capacity cannot exceed venue capacity"})

    def __str__(self):
        return self.title

    @property
    def registration_count(self):
        try:
            from apps.registrations.models import Registration
        except Exception:
            return None
        return Registration.objects.filter(event=self).count()


class Track(models.Model):
    """
    Tracks within an event (e.g., "Backend", "Frontend").
    Sessions are scheduled inside Tracks.
    """
    event = models.ForeignKey(Event, related_name="tracks", on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("event", "title")
        ordering = ["title"]

    def __str__(self):
        return f"{self.event.title} — {self.title}"


class Speaker(models.Model):
    """
    Speaker information. It can optionally link to an internal user.
    """
    user = models.ForeignKey(USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=255)
    bio = models.TextField(blank=True)
    website = models.URLField(blank=True)
    twitter = models.CharField(max_length=255, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Session(models.Model):
    """
    A session/talk inside a Track. Prevent overlapping sessions within the SAME track.
    Also ensures the session fits within the parent event's start/end dates.
    """
    track = models.ForeignKey(Track, related_name="sessions", on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    speaker = models.ForeignKey(Speaker, null=True, blank=True, on_delete=models.SET_NULL)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    room = models.CharField(max_length=100, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["start_time"]
        constraints = [
            models.CheckConstraint(check=models.Q(end_time__gt=models.F("start_time")), name="session_end_after_start"),
        ]

    def clean(self):
        if self.end_time <= self.start_time:
            raise ValidationError({"end_time": "end_time must be after start_time"})

        event = self.track.event
        if not (event.start_date <= self.start_time and self.end_time <= event.end_date):
            raise ValidationError("Session must be within parent event start_date and end_date")

        qs = Session.objects.filter(
            track=self.track,
        ).exclude(pk=self.pk).filter(
            start_time__lt=self.end_time,
            end_time__gt=self.start_time,
        )
        if qs.exists():
            raise ValidationError("Session overlaps with another session in the same track")

    def save(self, *args, **kwargs):
        with transaction.atomic():
            self.full_clean()
            super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} — {self.track}"

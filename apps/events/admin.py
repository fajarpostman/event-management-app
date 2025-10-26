from django.contrib import admin
from .models import Venue, Event, Track, Speaker, Session

@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    list_display = ("name", "capacity")
    search_fields = ("name", "address")

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "venue", "capacity", "start_date", "end_date")
    list_filter = ("venue",)
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ("title", "slug", "description")


@admin.register(Track)
class TrackAdmin(admin.ModelAdmin):
    list_display = ("title", "event")
    search_fields = ("title", "description")


@admin.register(Speaker)
class SpeakerAdmin(admin.ModelAdmin):
    list_display = ("name", "user")
    search_fields = ("name", "bio")


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ("title", "track", "start_time", "end_time", "room")
    list_filter = ("track__event",)
    search_fields = ("title", "description", "room")

import pytest
from django.contrib.auth import get_user_model
from apps.event.models import Venue, Event
from apps.registrations.models import Registration
from django.utils import timezone
from datetime import timedelta

User = get_user_model()

def test_prevent_over_capacity():
    v = Venue.objects.create(name='V', capacity=2)
    now = timezone.now()
    e = Event.objects.create(title='E', slug='e', venue=v, capacity=1, start_date=now, end_date=now+timedelta(hours=3))
    u1 = User.objects.create_user('u1', 'u1@example.com', 'pass')
    u2 = User.objects.create_user('u2', 'u2@example.com', 'pass')

    Registration.objects.create(attendee=u1, event=e)
    with pytest.raises(Exception):
        Registration.objects.create(attendee=u2, event=e)
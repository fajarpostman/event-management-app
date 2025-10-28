from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from apps.events.models import Venue, Event
from apps.registrations.models import Registration
from apps.users.models import User
from django.core.exceptions import ValidationError

class RegistrationTest(TestCase):
    def test_prevent_over_capacity(self):
        v = Venue.objects.create(name='Test Venue', capacity=2)
        now = timezone.now()
        e = Event.objects.create(
            title='Test Event', 
            venue=v, 
            capacity=1,
            start_date=now, 
            end_date=now + timedelta(hours=3)
        )

        u1 = User.objects.create_user('u1', 'u1@example.com', 'pass')
        u2 = User.objects.create_user('u2', 'u2@example.com', 'pass')

        Registration.objects.create(attendee=u1, event=e)

        with self.assertRaises(ValidationError):
            Registration.objects.create(attendee=u2, event=e)

        self.assertEqual(Registration.objects.count(), 1)

    def test_prevent_duplicate_registration(self):
        v = Venue.objects.create(name='Test Venue', capacity=2)
        now = timezone.now()
        e = Event.objects.create(
            title='Test Event 2',
            venue=v,
            capacity=2,
            start_date=now,
            end_date=now + timedelta(hours=3)
        )

        u1 = User.objects.create_user('u1', 'u1@example.com', 'pass')

        Registration.objects.create(attendee=u1, event=e)

        from django.db import IntegrityError
        with self.assertRaises(IntegrityError):
            Registration.objects.create(attendee=u1, event=e)

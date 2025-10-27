import pytest
from django.test import TestCase
from apps.events.models import Venue, Event
from apps.registrations.models import Registration
from apps.users.models import User
from django.utils import timezone
from datetime import timedelta

class RegistrationTest(TestCase):
    def test_prevent_over_capacity(self):
        v = Venue.objects.create(name='Test Venue', capacity=2)
        
        now = timezone.now()
        e = Event.objects.create(
            title='Test Event', 
            venue=v, 
            capacity=1,
            start_date=now, 
            end_date=now+timedelta(hours=3)
        )
        
        u1 = User.objects.create_user('u1', 'u1@example.com', 'pass')
        u2 = User.objects.create_user('u2', 'u2@example.com', 'pass')

        Registration.objects.create(user=u1, event=e)
        
        with self.assertRaises(Exception):
            Registration.objects.create(user=u2, event=e)
            
        self.assertEqual(Registration.objects.count(), 1)
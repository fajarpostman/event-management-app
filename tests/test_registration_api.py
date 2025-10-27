from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from apps.events.models import Event, Venue
from apps.registrations.models import Registration
from apps.users.models import User
from rest_framework_simplejwt.tokens import RefreshToken


class RegistrationAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='attendee', password='password123')
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

        # Create venue first
        self.venue = Venue.objects.create(
            name="Bali Conference Center",
            address="Bali, Indonesia",
            capacity=50
        )

        self.event = Event.objects.create(
            title="DjangoConf 2025", 
            description="Learn Django 5", 
            venue=self.venue, 
            capacity=50,
            start_date="2025-11-01T09:00:00Z", 
            end_date="2025-11-01T17:00:00Z"
        )
        self.url = reverse('registration-list')

    def test_register_attendee(self):
        payload = {"event": self.event.id}
        response = self.client.post(self.url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Registration.objects.count(), 1)

    def test_duplicate_registration_not_allowed(self):
        Registration.objects.create(user=self.user, event=self.event)
        payload = {"event": self.event.id}
        response = self.client.post(self.url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
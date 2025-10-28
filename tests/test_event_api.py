from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from apps.events.models import Event, Venue
from apps.users.models import User
from rest_framework_simplejwt.tokens import RefreshToken

class EventAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.user.is_staff = True
        self.user.is_organizer = True
        self.user.save()

        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        
        self.venue = Venue.objects.create(
            name="Conference Hall",
            address="123 Main St",
            capacity=200
        )
        
        self.event_url = reverse('event-list')

    def test_create_event(self):
        """Ensure we can create a new event."""
        payload = {
            "title": "Tech Conference 2025",
            "description": "A conference about the latest in tech.",
            "capacity": 200,
            "start_date": "2025-11-01T09:00:00Z",
            "end_date": "2025-11-01T17:00:00Z",
            "venue_id": self.venue.id
        }
        response = self.client.post(self.event_url, payload, format='json')
        print("❌ STATUS:", response.status_code)
        print("❌ RESPONSE:", response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Event.objects.count(), 1)

    def test_get_event_list(self):
        """Ensure we can list events."""
        Event.objects.create(
            title="Event 1",
            description="Description 1",
            venue=self.venue,
            capacity=100,
            start_date="2025-10-01T09:00:00Z", 
            end_date="2025-10-01T17:00:00Z"
        )
        response = self.client.get(self.event_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
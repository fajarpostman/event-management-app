from django.db import models, transaction
from django.conf import settings
from django.core.exceptions import ValidationError
from apps.events.models import Event

User = settings.AUTH_USER_MODEL

class Registration(models.Model):
    attendee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='registration')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='registrations')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('attendee', 'event')

    def clean(self):
        current_count = Registration.objects.filter(event=self.event).exclude(pk=self.pk).count()
        if current_count >= self.event.capacity:
            raise ValidationError("Event is full")

    def save(self, *args, **kwargs):
        with transaction.atomic():
            self.clean()
            super().save(*args, **kwargs)

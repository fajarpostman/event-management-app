from rest_framework import viewsets, permissions
from .models import Registration
from .serializers import RegistrationSerializer

class RegistrationViewSet(viewsets.ModelViewSet):
    serializer_class = RegistrationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if getattr(user, 'is_organizer', False):
            return Registration.objects.all()
        return Registration.objects.filter(attendee=user)
    
    def perform_create(self, serializer):
        serializer.save()

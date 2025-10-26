from rest_framework import serializers
from .models import Registration

class RegistrationSerializer(serializers.ModelSerializer):
    attendee = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())
    class Meta:
        model = Registration
        fields = ['id', 'attendee', 'event', 'created_at']
        read_only_fields = ['id', 'attendee', 'created_at']

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['attendee'] = user

        reg = Registration(**validated_data)
        reg.save()
        return reg
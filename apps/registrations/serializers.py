from rest_framework import serializers
from django.core.exceptions import ValidationError
from .models import Registration

class RegistrationSerializer(serializers.ModelSerializer):
    attendee = serializers.PrimaryKeyRelatedField(
        read_only=True,
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Registration
        fields = ['id', 'attendee', 'event', 'created_at']
        read_only_fields = ['id', 'attendee', 'created_at']

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['attendee'] = user

        reg = Registration(**validated_data)
        try:
            reg.save()
        except ValidationError as e:
            # Convert Django ValidationError menjadi DRF ValidationError agar jadi HTTP 400
            raise serializers.ValidationError(e.message_dict if hasattr(e, 'message_dict') else e.messages)
        return reg

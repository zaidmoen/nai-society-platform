from rest_framework import serializers
from .models import Profile

class RegistrationSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    password = serializers.CharField(min_length=10, write_only=True)
    first_name = serializers.CharField(max_length=150)
    last_name = serializers.CharField(max_length=150, required=False, allow_blank=True)
    university_id = serializers.CharField(max_length=32)
    phone = serializers.CharField(max_length=32, required=False, allow_blank=True)
    requested_role = serializers.ChoiceField(choices=Profile.RequestedRole.choices)
    requested_committee = serializers.CharField(max_length=80, required=False, allow_blank=True)


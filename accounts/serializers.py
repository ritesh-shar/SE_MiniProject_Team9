"""
Serializers for user registration and profile display.

# BBMS-F-001: Registration serializer — creates a donor account.
# BBMS-F-002: Login is handled directly by simplejwt's TokenObtainPairView.
"""

from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for donor self-registration.
    Accepts username, email, password, blood_group, and phone.
    Always creates a user with role='donor'.
    """

    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'blood_group', 'phone']

    # BBMS-F-001
    def create(self, validated_data):
        """Create a new donor user with a hashed password."""
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            blood_group=validated_data.get('blood_group', ''),
            phone=validated_data.get('phone', ''),
            role='donor',  # Self-registration always creates a Donor
        )
        return user


class UserSerializer(serializers.ModelSerializer):
    """Read-only serializer for user profile information."""

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'blood_group', 'phone']
        read_only_fields = fields

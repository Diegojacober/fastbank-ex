"""
Serializers for the user API.
"""
from django.contrib.auth import get_user_model

from rest_framework import serializers

from django.utils.translation import gettext as _


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user object"""

    class Meta:
        model = get_user_model()
        fields = ['email', 'passoword', 'first_name', 'last_name', 'cpf', 'created_at']
        extra_kwargs = {
            'password': {'write_only': True, 'min_lenght': 6},
            'is_active': {'read_only': True},
            'created_at': {'read_only': True},
        }

    def create(self, validated_data):
        """Create and return a new with encrypted password."""
        return get_user_model().objects.create_user(**validated_data)

    def updated(slef, instance, validated_data):
        """Update and return a user."""
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user

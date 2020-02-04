from django.contrib.auth import get_user_model

from rest_framework import serializers


USER = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user object"""

    class Meta:
        model = USER
        fields = ('email', 'password', 'name')
        extra_kwargs = {'password': {'write_only': True, 'min_length': 4}}

    def create(self, validated_data):
        """Create an user object with encrypted password and return it"""
        return USER.objects.create_user(**validated_data)

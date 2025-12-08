""""
Serializers for the user Api View.

In Python (and especially in Django/DRF), “serializers” are objects that convert complex data (like model instances) to and from simple, transferable formats (like JSON).

Typical jobs of a serializer:

Serialization (output)
Python objects → JSON (or dicts, XML, etc.) for APIs.
Deserialization (input)
JSON (or form data) → validated Python objects / models.
Validation
Check that incoming data is correct (types, required fields, custom rules).
"""

from rest_framework import serializers

from django.contrib.auth import (
    get_user_model,
    authenticate,
)

from django.utils.translation import gettext as _

# from django.contrib.auth.password_validation import validate_password

class UserSerializer(serializers.ModelSerializer):
    """Serializer for the users object"""

    class Meta:
        model = get_user_model()
        fields = ('email', 'password', 'name')
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    def create(self, validated_data):
        """Create and return a user with encrypted password"""
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """Update a user, setting the password correctly and return it"""
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user

class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user authentication token"""
    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False,
    )

    def validate(self, attrs):
        """Validate and authenticate the user"""
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password,
        )
        if not user:
            msg = _('Unable to authenticate with provided credentials')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs
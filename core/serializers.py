from djoser.serializers import UserCreateSerializer
from rest_framework.serializers import ModelSerializer, Serializer
from django.contrib.auth.password_validation import validate_password

from core.models import User
from rest_framework import serializers
from djoser.conf import settings


class UserRegistrationSerializer(UserCreateSerializer):
    """UserRegistrationSerializer has "re_password" field but front_api and
    swagger checking will be used "password_repeat in the query"""
    default_error_messages = {
        "password_mismatch": settings.CONSTANTS.messages.PASSWORD_MISMATCH_ERROR
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password_repeat"] = serializers.CharField(
            style={"input_type": "password"}
        )

    def validate(self, attrs):
        self.fields.pop("password_repeat", None)
        re_password = attrs.pop("password_repeat")
        attrs = super().validate(attrs)
        if attrs["password"] == re_password:
            return attrs
        else:
            self.fail("password_mismatch")

    class Meta:
        model = User
        fields = ["id", "username", "first_name", "last_name", "email", "password"]


class UserModelSerializer(UserCreateSerializer):

    class Meta:
        model = User
        fields = ["id", "username", "first_name", "last_name", "email", "password"]


class RetrieveUpdateProfileSerializer(ModelSerializer):
    read_only_fields = ["id"]
    class Meta:
        model = User
        fields = ["id", "username", "first_name", "last_name", "email"]


class ChangePasswordSerializer(Serializer):
    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_new_password(self, value):
        validate_password(value)
        return value

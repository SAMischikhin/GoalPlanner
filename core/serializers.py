from djoser.serializers import UserCreateSerializer

from core.models import User
from rest_framework import serializers
from djoser.conf import settings


class UserRegistrationSerializer(UserCreateSerializer):
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

    # '''UserRegistrationSerializer has "re_password" field but front_api and
    # swagger checking will be used "password_repeat in the query'''
    # def is_valid(self, raise_exception=False):
    #     self.initial_data["re_password"] = self.initial_data.pop("password_repeat")
    #     return super().is_valid(raise_exception=raise_exception)
    #
    class Meta:
        model = User
        fields = ["id", "username", "first_name", "last_name", "email", "password"]

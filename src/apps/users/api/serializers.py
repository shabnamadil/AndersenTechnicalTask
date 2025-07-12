from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

from rest_framework import serializers

from utils.serializers.helpers import PasswordField
from utils.serializers.mixins import PasswordConfirmationMixin

User = get_user_model()


class RegisterSerializer(PasswordConfirmationMixin, serializers.ModelSerializer):
    password = PasswordField(write_only=True, validators=[validate_password])
    password_confirm = PasswordField(write_only=True)

    class Meta:
        model = User
        fields = (
            "id",
            "first_name",
            "last_name",
            "username",
            "password",
            "password_confirm",
        )

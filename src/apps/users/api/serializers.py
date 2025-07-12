from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

from rest_framework import serializers

from utils.serializers.password_field import PasswordField

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
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

    def validate(self, attrs):
        password = attrs.get("password", "")
        password_confirm = self.initial_data.get("password_confirm", "")

        if not password_confirm:
            raise serializers.ValidationError(
                {
                    "password_confirm": "This field is required.",
                }
            )

        if password != password_confirm:
            raise serializers.ValidationError(
                {
                    "password_confirm": "Passwords do not match.",
                }
            )

        return attrs

    def create(self, validated_data):
        validated_data.pop("password_confirm")
        user = User.objects.create_user(**validated_data)
        return user

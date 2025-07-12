from rest_framework import serializers


class PasswordConfirmationMixin:
    def validate(self, attrs):
        password = attrs.get("password")
        password_confirm = self.initial_data.get("password_confirm")

        if not password_confirm:
            raise serializers.ValidationError(
                {"password_confirm": "This field is required."}
            )

        if password != password_confirm:
            raise serializers.ValidationError(
                {"password_confirm": "Passwords do not match."}
            )

        return attrs

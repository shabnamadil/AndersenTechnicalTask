from rest_framework import serializers


class PasswordField(serializers.CharField):
    def __init__(self, *args, **kwargs):
        kwargs["style"] = {"input_type": "password"}
        super().__init__(*args, **kwargs)

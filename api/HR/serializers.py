from rest_framework import serializers
from accounts.models import User
from django.contrib.auth.hashers import make_password
from rest_framework.validators import (
    UniqueValidator,
)  # used for field validator in the queryset


class EmployeeSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        validators=[UniqueValidator(User.objects.all())]  # Ensuring the email is unique
    )
    password = serializers.CharField(
        write_only=True,
        required=True,
        help_text="Leave empty if no change needed",
        style={"input_type": "password", "placeholder": "Password"},
    )

    class Meta:
        model = User
        fields = (
            "id",
            "first_name",
            "middle_name",
            "last_name",
            "username",
            "email",
            "password",
            "phone_number",
            "account",
        )

    def create(self, validated_data):
        validated_data["password"] = make_password(validated_data.get("password"))
        return super(EmployeeSerializer, self).create(validated_data)

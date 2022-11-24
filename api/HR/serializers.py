from rest_framework import serializers
from accounts.models import User , LeaveApplication , UserProfile
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

class UserprofileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('permanent_address','permanent_country','permanent_state','permanent_city','permanent_pincode','present_address','present_country','present_state','present_city','present_pincode','gender','emergency_contact','date_of_joining','date_of_termination','pan_card_no','aadhaar_card','blood_group','date_of_birth',)

class LeaveHRSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    def get_name(self,object):
        return object.user.get_fullname()  
    class Meta:
        model = LeaveApplication
        fields = ('id','name','date','reason','type','approved',)
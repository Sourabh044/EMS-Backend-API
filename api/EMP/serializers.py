from accounts.models import User, LeaveApplication, UserProfile
from rest_framework import serializers


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "first_name",
            "middle_name",
            "last_name",
            "username",
            "email",
            "phone_number",
            "account",
        )


class UserprofileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('permanent_address', 'permanent_country', 'permanent_state', 'permanent_city', 'permanent_pincode', 'present_address', 'present_country', 'present_state',
                  'present_city', 'present_pincode', 'gender', 'emergency_contact', 'date_of_joining', 'date_of_termination', 'pan_card_no', 'aadhaar_card', 'blood_group', 'date_of_birth',)


class EmpLeaveSerializer(serializers.ModelSerializer):
    approved = serializers.BooleanField(read_only=True)

    class Meta:
        model = LeaveApplication
        fields = ('id', 'approved', 'type', 'date', 'reason', 'user_id')
        depth = 1

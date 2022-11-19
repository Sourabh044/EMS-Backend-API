from accounts.models import User,LeaveApplication
from rest_framework import serializers

class EmpLeaveSerializer(serializers.ModelSerializer):
    approved = serializers.BooleanField(read_only=True)
    class Meta:
        model = LeaveApplication
        fields = ('id','approved','type','date','reason','user_id')
        depth = 1

    
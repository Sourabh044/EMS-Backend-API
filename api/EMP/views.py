from rest_framework import viewsets
from rest_framework.permissions import  IsAuthenticated
from accounts.models import LeaveApplication
from .serializers import EmpLeaveSerializer
from rest_framework.routers import DefaultRouter
from emp.utils import leave_apply_email

# Create your views here.

class EmpLeave(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return LeaveApplication.objects.filter(user=self.request.user)
    serializer_class = EmpLeaveSerializer
    
    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user.id)
        
router = DefaultRouter()

router.register(r'Leave',EmpLeave, basename='Leave')
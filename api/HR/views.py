from django.shortcuts import render
from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework import viewsets
from accounts.models import User
from api.HR.serializers import EmployeeSerializer
from rest_framework.routers import DefaultRouter
from django.contrib.auth.decorators import login_required ,permission_required , user_passes_test
# Create your views here.
# API Views

# Custom Permission to check if the user is the HR
class IsHR(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.account == 1


class EmployeeViewset(viewsets.ModelViewSet):
    queryset = User.objects.filter(account=2)
    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticated, IsHR]
    # authentication_classes = [TokenAuthentication]
    # renderer_classes = [UserRenderer]

router = DefaultRouter()

router.register(r'Employees',EmployeeViewset, basename='Employees')

from django.shortcuts import render 
from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework import viewsets
from accounts.models import User , LeaveApplication , UserProfile 
from api.HR.serializers import EmployeeSerializer ,LeaveHRSerializer , UserprofileSerializer
from rest_framework.routers import DefaultRouter
from rest_framework.response import Response
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
 

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        userprofile = UserProfile.objects.get(user=instance)
        userializer = UserprofileSerializer(instance=userprofile)
        serializer = self.get_serializer(instance)
        return Response({'user':serializer.data,
        'userprofile':userializer.data})

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        userprofile = UserProfile.objects.get(user=instance)
        userializer = UserprofileSerializer(userprofile,data=request.data,partial=partial)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True) and userializer.is_valid(raise_exception=True)
        # self.perform_update(serializer)
        serializer.save()
        userializer.save()

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response({'user':serializer.data,
        'userprofile':userializer.data})


class LeaveViewset(viewsets.ModelViewSet):
    queryset = LeaveApplication.objects.all()
    permission_classes = [IsAuthenticated,IsHR]
    serializer_class = LeaveHRSerializer
router = DefaultRouter()

router.register(r'Employees',EmployeeViewset, basename='Employees')
router.register(r'Leaves',LeaveViewset, basename='Leaves')

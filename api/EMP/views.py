from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from accounts.models import LeaveApplication
from .serializers import EmpLeaveSerializer, EmployeeSerializer, UserprofileSerializer
from rest_framework.routers import DefaultRouter
from accounts.models import User, UserProfile
# from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from django.db import transaction

# Create your views here.


class EmpLeave(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return LeaveApplication.objects.filter(user=self.request.user).order_by('-date')
    serializer_class = EmpLeaveSerializer

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user.id)


class EMPViewset(viewsets.ReadOnlyModelViewSet, mixins.UpdateModelMixin):
    permission_classes = [IsAuthenticated]
    serializer_class = EmployeeSerializer
    pagination_class = None

    def get_queryset(self):
        user = self.request.user
        queryset = User.objects.filter(pk=user.pk)
        return queryset

    def retrieve(self, request, *args, **kwargs):
        instance = request.user
        userprofile = UserProfile.objects.get(user=instance)
        userializer = UserprofileSerializer(instance=userprofile)
        serializer = self.get_serializer(instance)
        return Response({'user': serializer.data,
                         'userprofile': userializer.data})

    def list(self, request, *args, **kwargs):
        return self.retrieve(request)
        # userprofile = UserProfile.objects.get(user=request.user)
        # userializer = UserprofileSerializer(instance=userprofile)
        # serializer = self.get_serializer(request.user)
        # return Response({'user': serializer.data,
        #                  'userprofile': userializer.data})

    def update(self, request, *args, **kwargs):
        with transaction.atomic():
            partial = kwargs.pop('partial', False)
            instance = self.get_object()
            userprofile = UserProfile.objects.get(user=instance)
            userializer = UserprofileSerializer(
                userprofile, data=request.data, partial=partial)
            serializer = self.get_serializer(
                instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True) and userializer.is_valid(
                raise_exception=True)
            # self.perform_update(serializer)
            serializer.save()
            userializer.save()

            if getattr(instance, '_prefetched_objects_cache', None):
                # If 'prefetch_related' has been applied to a queryset, we need to
                # forcibly invalidate the prefetch cache on the instance.
                instance._prefetched_objects_cache = {}

            return Response({'user': serializer.data,
                            'userprofile': userializer.data})


router = DefaultRouter()

router.register(r'Leave', EmpLeave, basename='Leave')
router.register(r'', EMPViewset, basename='Leave')

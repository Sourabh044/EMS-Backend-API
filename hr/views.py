from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator
from accounts.views import check_role_HR
from accounts.models import User
from rest_framework import viewsets
from accounts.serializers import EmployeeSerializer
from rest_framework.permissions import IsAuthenticated, BasePermission
from accounts.forms import EmployeeForm
# Create your views here.

#API Views

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


@login_required(login_url='login')
@user_passes_test(check_role_HR)
def employee(request,pk=None):
    if not pk:
        employee_list = User.objects.filter(account=2)
        paginator = Paginator(employee_list,5) #show 10 employees only 

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return render(request,'hr/employees.html',{'page_obj': page_obj})
    elif pk:
        employee = User.objects.get(id=pk)
        form = EmployeeForm(instance=employee)
        context = {
            'form':form,
            'employee':employee,
        }
        return render(request,'hr/employee.html',context)
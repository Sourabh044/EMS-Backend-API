from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views import View
from rest_framework import viewsets
from rest_framework.permissions import BasePermission, IsAuthenticated

from accounts.forms import EmployeeForm, EmployeeUserProfileForm
from accounts.models import User, UserProfile
from accounts.serializers import EmployeeSerializer
from accounts.views import check_role_HR

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


# @login_required(login_url='login')
# @user_passes_test(check_role_HR)
# def employee(request,pk=None):
#     if not pk:
#         employee_list = User.objects.filter(account=2).order_by('-date_joined')
#         paginator = Paginator(employee_list,5) #show 5 employees only 

#         page_number = request.GET.get('page')
#         page_obj = paginator.get_page(page_number)

#         return render(request,'hr/employees.html',{'page_obj': page_obj})
#     elif pk:
#         employee = User.objects.get(id=pk)
#         profile = UserProfile.objects.get(user=employee)
#         if request.method == 'POST':
#             form = EmployeeForm(request.POST,instance=employee)
#             pform = EmployeeUserProfileForm(request.POST,instance=profile)
#             if form.is_valid() and pform.is_valid():
#                 form.save()
#                 pform.save()
#                 messages.success(request,f'Employee {employee} updated!')
#         form = EmployeeForm(instance=employee)
#         pform = EmployeeUserProfileForm(instance=profile)
#         context = {
#             'form':form,
#             'pform': pform,
#             'employee':employee,
#         }
#         return render(request,'hr/employee.html',context)

# @login_required(login_url='login')
# @user_passes_test(check_role_HR)
decorators = [login_required,user_passes_test(check_role_HR)]
@method_decorator(decorators,name='get')
class Employee(View):

    def get(self,request,pk=None):
        if not pk:
            employee_list = User.objects.filter(account=2).order_by('-date_joined')
            paginator = Paginator(employee_list,1) #show 5 employees only 

            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)

            return render(request,'hr/employees.html',{'page_obj': page_obj})
        elif pk:
            employee = User.objects.get(id=pk)
            profile = UserProfile.objects.get(user=employee)
            form = EmployeeForm(instance=employee)
            pform = EmployeeUserProfileForm(instance=profile)
            context = {
                'form':form,
                'pform': pform,
                'employee':employee,
            }
            return render(request,'hr/employee.html',context)

    def post(self,request,pk= None):
        employee = User.objects.get(id=pk)
        profile = UserProfile.objects.get(user=employee)
        form = EmployeeForm(request.POST,instance=employee)
        pform = EmployeeUserProfileForm(request.POST,instance=profile)
        if form.is_valid() and pform.is_valid():
            form.save()
            pform.save()
            messages.success(request,f'Employee {employee} updated!')
        form = EmployeeForm(instance=employee)
        pform = EmployeeUserProfileForm(instance=profile)
        context = {
            'form':form,
            'pform': pform,
            'employee':employee,
        }
        return render(request,'hr/employee.html',context)     

def deleteEmployee(request,pk=None):
        if pk:
            employee = User.objects.get(pk=pk)
            employee.delete()
            messages.success(request,f'SuccessFully deleted {employee}')
            return redirect('employees')
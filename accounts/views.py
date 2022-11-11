from django.shortcuts import redirect, render
from rest_framework import viewsets
from accounts.serializers import EmployeeSerializer
from .models import User
from rest_framework.permissions import IsAuthenticated, BasePermission

from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator


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

# ------------------------------------------------------------------------------------------------------------------------

def check_role_HR(user):
    try:
        if user.account == 1:
            return True
        else:
            raise PermissionDenied
    except:
        raise PermissionDenied


# Restrict the Vendor from accessing the Customer
def check_role_employee(user):
    try:
        if user.account == 2:
            return True
        else:
            raise PermissionDenied
    except:
        raise PermissionDenied


def home(request):
    if request.user.is_authenticated:
        if request.user.account == 1:
            template = "basehr.html"
        elif request.user.account == 1:
            template = "baseemp.html"
        elif request.user.account == None and request.user.is_superadmin:
            return redirect("/admin")
    else:
        template = "login.html"
    return render(request, template)


def login(request):
    if not request.user.is_anonymous:
        return redirect("home")
    if request.method == "POST":
        email = request.POST.get("email")
        psw = request.POST.get("psw")
        user = auth.authenticate(email=email, password=psw)
        if not user is None:
            auth.login(request, user)
            messages.success(request, "You are now logged in")
            return redirect("home")
        else:
            messages.error(request, "Invalid Login Credenatials")
            return redirect("login")
    else:
        return render(request, "login.html")


def logout(request):
    auth.logout(request)
    return redirect("home")


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
        pass
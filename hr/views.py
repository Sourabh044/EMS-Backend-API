from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views import View


from django.views.generic.edit import CreateView
from accounts.forms import EmployeeForm, EmployeeUserProfileForm, LeaveForm
from accounts.models import User, UserProfile, LeaveApplication
from accounts.views import check_role_HR
from django.views import View
from django.contrib.auth.hashers import make_password
from .utils import leave_email

# Create your views here.

"""@login_required(login_url='login')
@user_passes_test(check_role_HR)
def employee(request,pk=None):
    if not pk:
        employee_list = User.objects.filter(account=2).order_by('-date_joined')
        paginator = Paginator(employee_list,5) #show 5 employees only

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return render(request,'hr/employees.html',{'page_obj': page_obj})
    elif pk:
        employee = User.objects.get(id=pk)
        profile = UserProfile.objects.get(user=employee)
        if request.method == 'POST':
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

@login_required(login_url='login')
@user_passes_test(check_role_HR)"""


decorators = [login_required, user_passes_test(check_role_HR)]


@method_decorator(decorators, name="get")
class Employee(View):
    # To Fetch a All employees or to fetch a single Employee using pk
    def get(self, request, pk=None):
        if not pk:
            employee_list = User.objects.filter(account=2).order_by("-date_joined")
            paginator = Paginator(
                employee_list,
            )  # show 5 employees only

            page_number = request.GET.get("page")
            page_obj = paginator.get_page(page_number)

            return render(request, "hr/employees.html", {"page_obj": page_obj})
        elif pk:
            employee = User.objects.get(id=pk)
            profile = UserProfile.objects.get(user=employee)
            form = EmployeeForm(instance=employee)
            pform = EmployeeUserProfileForm(instance=profile)
            context = {
                "form": form,
                "pform": pform,
                "employee": employee,
            }
            return render(request, "hr/employee.html", context)

    # To Update a employee
    def post(self, request, pk=None):
        employee = User.objects.get(id=pk)
        profile = UserProfile.objects.get(user=employee)
        form = EmployeeForm(request.POST, instance=employee)
        pform = EmployeeUserProfileForm(request.POST, instance=profile)
        if form.is_valid() and pform.is_valid():
            form.save()
            pform.save()
            messages.success(request, f"Employee {employee} updated!")
        form = EmployeeForm(instance=employee)
        pform = EmployeeUserProfileForm(instance=profile)
        context = {
            "form": form,
            "pform": pform,
            "employee": employee,
        }
        return render(request, "hr/employee.html", context)


def deleteEmployee(request, pk=None):
    if pk:
        employee = User.objects.get(pk=pk)
        employee.delete()
        messages.success(request, f"SuccessFully deleted {employee}")
        return redirect("employees")


def addemployee(request):
    if request.method == "POST":
        form = EmployeeForm(request.POST)
        pform = EmployeeUserProfileForm(request.POST)
        if form.is_valid() and pform.is_valid():
            employee = form.save(commit=False)
            employee.account = User.EMPLOYEE
            employee.password = make_password(request.POST.get("password"))
            employee.save()
            pform.save()
            messages.success(request, f"Employee Saved")
            return redirect("employees")
        else:
            context = {"form": form, "pform": pform}
            return render(request, "hr/addemployee.html", context)
    form = EmployeeForm()
    pform = EmployeeUserProfileForm()
    context = {"form": form, "pform": pform}
    return render(request, "hr/addemployee.html", context)


def LeaveList(request, pk=None):
    if pk:
        leave = LeaveApplication.objects.get(id=pk)
        if request.method == "POST":
            form = LeaveForm(request.POST)
            if form.is_valid():
                approved = form.cleaned_data.get("approved")
                leave.approved = approved
                leave.date = form.cleaned_data.get("date")
                leave.reason = form.cleaned_data.get("reason")
                leave.type = form.cleaned_data.get("type")
                leave.save()
                user = leave.user
                if approved:
                    messages.success(
                        request, f"{leave.user.first_name} Leave has Been Granted."
                    )
                else:
                    messages.error(
                        request, f"{leave.user.first_name} Leave has Been Denied!"
                    )
                return redirect("leave-list")
        form = LeaveForm(instance=leave)
        context = {
            "leave": leave,
            "form": form,
        }

        return render(request, "hr/leave.html", context)
    leaves = LeaveApplication.objects.all()
    paginator = Paginator(leaves, 10)  # show 5 employees only

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {
        "leaves": leaves,
        "page_obj": page_obj,
    }

    return render(request, "hr/leavelist.html", context)

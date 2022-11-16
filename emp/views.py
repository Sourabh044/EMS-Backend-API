from django.contrib import messages
from django.contrib.auth.decorators import (
    login_required,
    permission_required,
    user_passes_test,
)
from django.shortcuts import render, redirect
from accounts.forms import LeaveForm
from accounts.models import LeaveApplication
from accounts.views import check_role_employee


# Create your views here.
@login_required(login_url="login")
@user_passes_test(check_role_employee)
def myleaves(request):
    user = request.user
    leaves = LeaveApplication.objects.filter(user=user).order_by("-date")
    if leaves.exists():
        context = {
            "leaves": leaves,
        }
        return render(request, "emp/leaves.html", context)
    else:
        return render(request, "emp/leaves.html")


def applyleave(request):
    if request.method == "POST":
        request.POST._mutable = True
        request.POST["type"] = 2
        request.POST._mutable = False
        form = LeaveForm(request.POST)
        if form.is_valid():
            leave = form.save(commit=False)
            leave.user = request.user
            leave.save()
            messages.success(request, "Success: Wait for Approval.")
            return redirect("my-leaves")
        else:
            print(form.errors)
    form = LeaveForm()
    context = {
        "form": form,
    }
    return render(request, "emp/applyleave.html", context)

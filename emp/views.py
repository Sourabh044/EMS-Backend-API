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
    print(user)
    leaves = LeaveApplication.objects.filter(user=user).order_by("-date")
    if leaves.exists():
        print(leaves)
        context = {
            "leaves": leaves,
        }
    else:
        context = {}
    return render(request, "emp/leaves.html", context)


def applyleave(request):
    if request.method == "POST":
        request.POST._mutable = True
        data = request.POST
        data['type'] = 2
        request.POST._mutable = False
        form = LeaveForm(data)
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

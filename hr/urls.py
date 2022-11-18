from django.urls import path
from django.shortcuts import redirect,render
from .views import *
from django.contrib.auth.decorators import login_required ,permission_required , user_passes_test

urlpatterns = [
    path('employees',login_required( user_passes_test(Employee.as_view())), name='employees'),
    path('employees/<int:pk>',login_required(Employee.as_view()), name='employee'),
    path('employees/delete/<int:pk>',deleteEmployee, name='delete-employee'),
    path('addemployee/',addemployee,name='add-employee'),
    path('leavelist/',LeaveList,name='leave-list'),
    path('leave/<int:pk>',LeaveList,name='leave'),
]

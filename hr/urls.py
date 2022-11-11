from django.urls import path
from django.shortcuts import redirect,render
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r'Employees',EmployeeViewset, basename='Employees')

urlpatterns = [
    path('employees',employee, name='employees'),
    path('employees/<int:pk>',employee, name='employee'),
]

urlpatterns += router.urls
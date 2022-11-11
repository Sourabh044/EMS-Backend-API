from django.urls import path
from django.shortcuts import redirect,render
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r'Employees',EmployeeViewset, basename='Employees')

urlpatterns = [
    path('',home,name=''),
    path('home',home, name='home'),
    path('login',login, name='login'),
    path('logout',logout, name='logout'),
    path('employees',employee, name='employees'),

]

urlpatterns += router.urls
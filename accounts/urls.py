from django.urls import path
from django.shortcuts import redirect,render
from .views import *

urlpatterns = [
    path('',home,name=''),
    path('home',home, name='home'),
    path('login',login, name='login'),
    path('logout',logout, name='logout'),
    path('employees',employee, name='employees'),

]

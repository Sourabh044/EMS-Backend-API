from django.urls import path
from django.shortcuts import redirect,render
from .views import *
from rest_framework.routers import DefaultRouter
from django.contrib.auth.decorators import login_required ,permission_required , user_passes_test


urlpatterns = [

    path('my-leaves/',myleaves,name='my-leaves'),
    path('apply-leave/',applyleave,name='apply-leave'),
]
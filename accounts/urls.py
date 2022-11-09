from django.urls import path
from django.shortcuts import redirect,render
from .views import *


urlpatterns = [
    path('',home, name='home')
]
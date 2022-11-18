from django.urls import path , include
from rest_framework.routers import DefaultRouter
import api.HR.views
urlpatterns = [
    path('HR/',include(api.HR.views.router.urls),name='HR-api')
]
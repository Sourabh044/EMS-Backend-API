from django.urls import path, include
from rest_framework.routers import DefaultRouter
import api.HR.views
import api.EMP.views
urlpatterns = [
    path('HR/', include(api.HR.views.router.urls)),
    path('EMP/', include(api.EMP.views.router.urls)),
]

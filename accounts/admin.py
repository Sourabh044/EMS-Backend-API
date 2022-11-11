from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *
# Register your models here.
class CustomUserAdmin(UserAdmin):
    list_display = ("username", "first_name", "last_name", "account", "is_active")
    ordering = ("-date_joined",)
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(User, CustomUserAdmin)

# class CustomUserProfileAdmin(UserAdmin):
#     list_display = ("email", "first_name", "last_name", "role", "is_active")
#     ordering = ("-date_joined",)
#     filter_horizontal = ()
#     list_filter = ()
#     fieldsets = ()

admin.site.register(UserProfile)

admin.site.register(EducationDetails)
admin.site.register(LeaveApplication)
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import *


# Register your models here.


@admin.action(description="Mark selected as Active")
def make_active(modeladmin, request, queryset):
    queryset.update(is_active=True)

@admin.action(description="Mark selected as InActive")
def make_inactive(modeladmin, request, queryset):
    queryset.update(is_active=False)


class CustomUserAdmin(UserAdmin):
    list_display = ("username", "first_name", "last_name", "account", "is_active")
    ordering = ("-date_joined",)
    actions = [make_active,make_inactive]
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
    list_per_page = 20


admin.site.register(User, CustomUserAdmin)

# class CustomUserProfileAdmin(UserAdmin):
#     list_display = ("email", "first_name", "last_name", "role", "is_active")
#     ordering = ("-date_joined",)
#     filter_horizontal = ()
#     list_filter = ()
#     fieldsets = ()

admin.site.register(UserProfile)

admin.site.register(EducationDetails)


class LeaveAppAdmin(admin.ModelAdmin):
    search_fields = ("user__username", "date")
    list_display = ("user", "date", "approved", "type")
    list_display_links = ("user",)
    list_editable = ("approved", "type")
    ordering = ("-date",)
    date_hierarchy = "date"


admin.site.register(LeaveApplication, LeaveAppAdmin)

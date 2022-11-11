from django import forms
from .models import User


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = User
        # fields = ('first_name',)
        exclude = ("password","date_joined", "last_login", "created_at", "modified_date",'is_admin','is_staff','is_superadmin','is_active',)


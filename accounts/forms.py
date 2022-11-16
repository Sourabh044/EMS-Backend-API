from django import forms
from .models import User ,UserProfile , LeaveApplication

class DateInput(forms.DateInput):
    input_type = 'date'

class EmployeeForm(forms.ModelForm):    
    class Meta:
        model = User
        # fields = ('first_name',)
        exclude = (
            "password",
            "date_joined",
            "last_login",
            "created_at",
            "modified_date",
            "is_admin",
            "is_staff",
            "is_superadmin",
            "is_active",
        )


class EmployeeUserProfileForm(forms.ModelForm):
    date_of_joining = forms.DateField(required= False, widget=DateInput)
    date_of_termination = forms.DateField(required= False, widget=DateInput)
    date_of_birth = forms.DateField(required= False, widget=DateInput)
    class Meta:
        model = UserProfile
        fields = (
            # 'profile_picture',
            "permanent_address",
            "permanent_pincode",
            "present_address",
            "present_pincode",
            "gender",
            "emergency_contact",
            "date_of_joining",
            "date_of_termination",
            "pan_card_no",
            "aadhaar_card",
            "blood_group",
            "date_of_birth",
        )

class LeaveForm(forms.ModelForm):
    date = forms.DateField(required= False, widget=DateInput)
    class Meta:
        model = LeaveApplication
        fields = ('approved','type','date','reason',)
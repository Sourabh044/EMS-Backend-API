from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# from django.utils.translation import ugettext_lazy as _
import datetime
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.


class UserManager(BaseUserManager):
    def create_user(self, first_name, last_name, username, email, password=None):
        if not email:
            raise ValueError("User must provide an Email.")
        if not username:
            raise ValueError("User must provide an Username.")

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, last_name, username, email, password=None):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
            password=password,
        )

        user.is_admin = True
        user.is_active = True
        user.is_superadmin = True
        user.is_staff = True
        user.save(using=self._db)


class User(AbstractBaseUser):
    HR = 1
    EMPLOYEE = 2

    ROLE_CHOICE = (
        (HR, "HR"),
        (EMPLOYEE, "EMPLOYEE"),
    )
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=12, blank=True)
    account = models.PositiveSmallIntegerField(
        choices=ROLE_CHOICE, blank=True, null=True
    )
    # Required Fields

    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "first_name", "last_name"]

    objects = UserManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_lable):
        return True

    def get_role(self):
        if self.account == 1:
            user_role = "HR"
        elif self.account == 2:
            user_role = "EMPLOYEE"
        return user_role


class UserProfile(models.Model):
    MALE = 1
    FEMALE = 2

    GENDER_CHOICES = (
        (MALE, "Male"),
        (FEMALE, "Female"),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    profile_picture = models.ImageField(
        upload_to="user/profile_pictures", blank=True, null=True
    )
    cover_photo = models.ImageField(
        upload_to="user/cover_photos", blank=True, null=True
    )

    # Address Details
    permanent_address = models.CharField(max_length=250, blank=True, null=True)
    permanent_country = models.CharField(max_length=15, blank=True, null=True)
    permanent_state = models.CharField(max_length=15, blank=True, null=True)
    permanent_city = models.CharField(max_length=15, blank=True, null=True)
    permanent_pincode = models.CharField(max_length=6, blank=True, null=True)
    present_address = models.CharField(max_length=250, blank=True, null=True)
    present_country = models.CharField(max_length=15, blank=True, null=True)
    present_state = models.CharField(max_length=15, blank=True, null=True)
    present_city = models.CharField(max_length=15, blank=True, null=True)
    present_pincode = models.CharField(max_length=6, blank=True, null=True)

    # Personal Details
    gender = models.PositiveSmallIntegerField(
        choices=GENDER_CHOICES, blank=True, null=True
    )
    emergency_contact = models.CharField(max_length=12, blank=True, null=True)
    date_of_joining = models.DateTimeField(blank=True, null=True)
    date_of_termination = models.DateTimeField(blank=True, null=True)
    pan_card_no = models.CharField(max_length=15, blank=True, null=True)
    aadhaar_card = models.CharField(max_length=20, blank=True, null=True)
    blood_group = models.CharField(max_length=20, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)

    # Extra - Details
    latitude = models.CharField(max_length=20, blank=True, null=True)
    longitude = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    # def get_fulladdress(self):
    #     return f'{self.address_line_1} , {self.address_line_2}'

    def __str__(self) -> str:
        return self.user.email


def current_year():
    return datetime.date.today().year


def max_value_current_year(value):
    return MaxValueValidator(current_year())(value)


def year_choices():
    return [(r, r) for r in range(1984, datetime.date.today().year + 1)]


# class MyForm(forms.ModelForm):
#     year = forms.TypedChoiceField(coerce=int, choices=year_choices, initial=current_year)


class EducationDetails(models.Model):

    name = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    degree = models.CharField(max_length=50, blank=True, null=True)
    details = models.TextField(max_length=150)
    grade = models.CharField(max_length=50, blank=True, null=True)
    passing_year = models.IntegerField(
        validators=[MinValueValidator(1984), max_value_current_year]
    )
    certificate = models.FileField(upload_to="pdfs/", null=True, blank=True)

    class Meta:
        verbose_name_plural = "Education Details"


class LeaveApplication(models.Model):
    PAID = 1
    UNPAID = 2

    LEAVE_TYPE = (
        (PAID,'PAID'),
        (UNPAID,"UNPAID"),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(blank=False, null=False)
    reason = models.TextField(max_length=150,null=True,blank=True)
    type = models.PositiveSmallIntegerField(choices=LEAVE_TYPE,default=UNPAID)
    approved = models.BooleanField(default=False)



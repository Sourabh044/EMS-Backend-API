from django.db.models.signals import post_save, pre_save
from .models import User, UserProfile, LeaveApplication
from django.dispatch import receiver
from emp.utils import leave_apply_email
from hr.utils import leave_email
from django.contrib.sites.models import Site


@receiver(post_save, sender=User)
def post_save_create_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    else:
        try:
            profile = UserProfile.objects.get(user=instance)
            profile.save()
        except:
            # creating new user profile
            UserProfile.objects.create(user=instance)


@receiver(pre_save, sender=User)
def pre_save_profile_reciever(sender, instance, **kwargs):
    # print(instance.username, "user is being saved")
    pass


# post_save.connect(post_save_create_profile, sender=User)


# @receiver(post_save, sender=LeaveApplication)
# def post_save_leave_reciever(sender, instance, created, **kwargs):
#     if created:
#         mail_subject = "Leave Applied Successfully!"
#         template_name = "emails/emp/leaveapply.html"
#         user = instance.user
#         site = Site.objects.get_current()
#         request = {
#             "scheme": "https",
#             "get_host": site.domain,
#         }
#         try:
#             leave_apply_email(
#                 request,
#                 user,
#                 instance,
#                 mail_subject,
#                 template_name,
#             )
#         except Exception as e:
#             print(e)
#     else:
#         pass


# @receiver(pre_save, sender=LeaveApplication)
# def pre_save_leave_application(sender, instance, *args, **kwargs):
#     if instance.pk:
#         original = LeaveApplication.objects.get(pk=instance.pk)
#         user = instance.user
#         site = Site.objects.get_current()
#         request = {
#             "scheme": "https",
#             "get_host": site.domain,
#         }
#         if instance.approved == True and original.approved != True:
#             mail_subject = "Leave Approved!!"
#             template_name = "emails/hr/leaveapprove.html"
#         else:
#             mail_subject = "Sorry!!"
#             template_name = "emails/hr/leavedenied.html"
#         try:
#             leave_email(request, user, instance, mail_subject, template_name)
#         except Exception as e:
#             print(e)
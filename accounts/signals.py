from django.db.models.signals import post_save, pre_save
from .models import User, UserProfile
from django.dispatch import receiver
# from django.contrib import messages

@receiver(post_save, sender=User)
def post_save_create_profile(sender, instance, created, **kwargs):
    # print(kwargs)
    if created:
        UserProfile.objects.create(user=instance)
        # messages.success(kwargs['request'], "Your Account has been created.")
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

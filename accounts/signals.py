from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import User, UserProfile

@receiver(post_save, sender=User)
def post_save_create_profile_receiver(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    else:
        try:
            profile_instance = UserProfile.objects.get(user=instance)
            profile_instance.save()
        except:
            UserProfile.objects.create(user=instance)

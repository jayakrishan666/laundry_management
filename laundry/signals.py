from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Ensure a UserProfile is created when a new User is registered."""
    if created:
        UserProfile.objects.create(user=instance)

from django.db.models.signals import post_save
from django.dispatch import receiver

from django.contrib.auth.models import User
from profiles.models import Profile


@receiver(post_save, sender=User)
def handle_user_save(sender, created, instance, **kwargs):
    print sender
    print created
    print instance
    print kwargs
    if created:
        Profile.objects.create(user=instance)




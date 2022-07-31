from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import User
from .utils import send_confirmation_mail


@receiver(post_save, sender=User)
def create_user_profile_and_mail(instance: User, created, raw, **kwargs):
    """Send a welcome mail to recent created User."""
    if created is True:
        instance.set_password(instance.password)
        instance.save(update_fields=['password'])
        send_confirmation_mail(instance)

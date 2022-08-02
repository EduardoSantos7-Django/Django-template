from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import User


@receiver(post_save, sender=User)
def create_user_profile(instance: User, created, raw, **kwargs):
    """
    Create the User related Profile.
    """
    # FIXME: Not implemented
    # if created:
    #     # "raw" param means "created with manage.py loaddata"
    #     if raw:
    #         instance.set_password(instance.password)
    #         instance.save()
    #     else:
    #         # Raw users already have their own profile instances
    #         Profile.objects.create_profile(instance)

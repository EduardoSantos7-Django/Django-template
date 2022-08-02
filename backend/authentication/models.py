from django.contrib.auth.models import AbstractUser
from django.db import models

from utils.models import generate_pk_base_64

from .managers import UserManager


def user_pk():
    return generate_pk_base_64(User)


class User(AbstractUser):
    """
    Overide default User model.
    """

    # Override properties
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    objects = UserManager()

    # Override fields
    username = None
    id = models.CharField(
        primary_key=True, max_length=11, default=user_pk, editable=False
    )
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)

    # New fields
    email_verified = models.BooleanField(default=False)

    def __str__(self) -> str:
        full_name = self.first_name
        if self.last_name:
            full_name += ' ' + self.last_name
        return full_name

    class Meta:
        ordering = ['date_joined']

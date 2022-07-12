from django.contrib import auth
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

from utils.models import generate_pk_base_64


def user_pk():
    return generate_pk_base_64(User)


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password, **extra_fields):
        """Create and save a user with the given, email, and password."""

        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email=None, password=None, **extra_fields):
        """Create and save a superuser with the given, email, and password."""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)

    def with_perm(
        self, perm, is_active=True, include_superusers=True, backend=None, obj=None
    ):
        if backend is None:
            backends = auth._get_backends(return_tuples=True)
            if len(backends) == 1:
                backend, _ = backends[0]
            else:
                raise ValueError(
                    "You have multiple authentication backends configured and "
                    "therefore must provide the `backend` argument."
                )
        elif not isinstance(backend, str):
            raise TypeError(
                "backend must be a dotted import path string (got %r)." % backend
            )
        else:
            backend = auth.load_backend(backend)
        if hasattr(backend, "with_perm"):
            return backend.with_perm(
                perm,
                is_active=is_active,
                include_superusers=include_superusers,
                obj=obj,
            )
        return self.none()


class User(AbstractUser):
    """Overide default User model."""

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
    email_verified = models.BooleanField(default=True)

    def __str__(self) -> str:
        full_name = self.first_name
        if self.last_name:
            full_name += ' ' + self.last_name
        return full_name

    class Meta:
        ordering = ['date_joined']

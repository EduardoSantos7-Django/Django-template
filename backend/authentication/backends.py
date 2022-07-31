from .models import User
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q


class EmailBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        if email is None:
            email = kwargs.get(User.USERNAME_FIELD, kwargs.get(User.EMAIL_FIELD))
        if email is None or password is None:
            return
        try:
            user: User = User._default_manager.get(
                Q(email=email) & Q(email_verified=True)
            )
        except User.DoesNotExist:
            return
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user

from django.contrib.auth.backends import ModelBackend
from django.db.models import Q

from .models import User


class EmailBackend(ModelBackend):
    def authenticate(  # pylint: disable=W0237
        self, request, email=None, password=None, **kwargs
    ):
        if email is None:
            email = kwargs.get('username', kwargs.get('email'))
        if email is None or password is None:
            return None
        try:
            user: User = User._default_manager.get(
                Q(email=email) & Q(email_verified=True)
            )
        except User.DoesNotExist:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a nonexistent user (#20760).
            User().set_password(password)
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
        return None

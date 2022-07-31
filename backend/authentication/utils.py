from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from .models import User


class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user: User, timestamp):
        return f'{user.email}{timestamp}{user.email_verified}'


def send_confirmation_mail(instance: User):
    token_generator = TokenGenerator()
    domain = 'http://127.0.0.1:8000'  # FIXME: Get domain dynamically

    uid = urlsafe_base64_encode(force_bytes(instance.email))
    token = token_generator.make_token(instance)

    subject = 'Please, confirm your email'
    message = '{domain}/verify/{uid}/{token}'.format(
        domain=domain, uid=uid, token=token
    )

    send_mail(
        subject=subject,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[instance.email],
        fail_silently=False,
    )

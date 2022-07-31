from django.conf import settings
from django.contrib.auth.tokens import (
    default_token_generator as password_reset_token_generator,
)
from django.core.mail import send_mail
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from .tokens import confirm_email_token_generator


def send_confirmation_mail(request, instance):
    uidb64 = urlsafe_base64_encode(force_bytes(instance.email))
    token = confirm_email_token_generator.make_token(instance)

    domain = request.build_absolute_uri('/')

    subject = 'Please, confirm your email'
    message = f'{domain}account/email/confirm/{uidb64}/{token}/'

    send_mail(
        subject=subject,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[instance.email],
        fail_silently=False,
    )


def send_reset_password_mail(request, instance):
    uidb64 = urlsafe_base64_encode(force_bytes(instance.email))
    token = password_reset_token_generator.make_token(instance)

    domain = request.build_absolute_uri('/')

    subject = 'Please, reset your password'
    message = f'{domain}account/password/reset/{uidb64}/{token}/'

    send_mail(
        subject=subject,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[instance.email],
        fail_silently=False,
    )

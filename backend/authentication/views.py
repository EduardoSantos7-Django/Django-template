from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.tokens import (
    default_token_generator as password_reset_token_generator,
)
from django.http import Http404
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from drf_spectacular.utils import OpenApiParameter, extend_schema, extend_schema_view
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from . import serializers
from .models import User
from .tokens import confirm_email_token_generator
from .utils import send_confirmation_email, send_reset_password_email


@extend_schema_view(
    sign_in=extend_schema(
        summary='Sign in user',
        request=serializers.UserIn,
        responses=serializers.User,
        tags=['authentication'],
    ),
    sign_out=extend_schema(
        summary='Sign out user',
        request=None,
        responses={status.HTTP_204_NO_CONTENT: None},
        tags=['authentication'],
    ),
    sign_up=extend_schema(
        summary='Sign up user',
        request=serializers.UserUp,
        responses={status.HTTP_201_CREATED: serializers.User},
        tags=['authentication'],
    ),
)
class AuthViewSet(GenericViewSet):
    """Viewset with services to authentication and user session control."""

    serializer_class = serializers.User

    @action(['POST'], detail=False, url_path='sign-in')
    def sign_in(self, request):
        """Sign user in session."""
        serializer = serializers.UserIn(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.data
        user = authenticate(**data)
        if user is not None:
            login(request, user)
            if not data.get('remember_me'):
                request.session.set_expiry(0)
            serializer = self.get_serializer(user)
            return Response(data, status=status.HTTP_200_OK)

        # Verify if user exists and not confirmed your email
        try:
            user: User = User.objects.get(email=data['email'], email_verified=False)
            return Response('User email not confirmed', status.HTTP_403_FORBIDDEN)
        except User.DoesNotExist:
            return Response('User not found.', status=status.HTTP_404_NOT_FOUND)

    @action(['POST'], detail=False, url_path='sign-out')
    def sign_out(self, request):
        """Sign user out in session."""
        logout(request)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(['POST'], detail=False, url_path='sign-up')
    def sign_up(self, request):
        """Sign user up in DB."""
        serializer = serializers.UserUp(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.create(serializer.validated_data)
        data = self.get_serializer(user).data

        send_confirmation_email(request, user)

        return Response(data, status=status.HTTP_201_CREATED)


@extend_schema_view(
    resend_confirmation_email=extend_schema(
        summary='Resend confirmation email if account exists',
        request=serializers.SendEmail,
        responses={
            status.HTTP_204_NO_CONTENT: None,
        },
        tags=['authentication'],
    ),
    confirm_email=extend_schema(
        summary='Confirm user email',
        parameters=[
            OpenApiParameter(name='uidb64', type=str, location=OpenApiParameter.PATH),
            OpenApiParameter(name='token', type=str, location=OpenApiParameter.PATH),
        ],
        request=None,
        responses={
            status.HTTP_204_NO_CONTENT: None,
            status.HTTP_404_NOT_FOUND: None,
        },
        tags=['authentication'],
    ),
    send_reset_password_email=extend_schema(
        summary='Send reset email if a related account exists',
        request=serializers.SendEmail,
        responses={
            status.HTTP_204_NO_CONTENT: None,
        },
        tags=['authentication'],
    ),
    reset_password=extend_schema(
        summary='Reset password',
        parameters=[
            OpenApiParameter(name='uidb64', type=str, location=OpenApiParameter.PATH),
            OpenApiParameter(name='token', type=str, location=OpenApiParameter.PATH),
        ],
        request=serializers.ChangePassord,
        responses={
            status.HTTP_204_NO_CONTENT: None,
        },
        tags=['authentication'],
    ),
)
class AuthTokenViewset(GenericViewSet):
    def get_serializer_class(self):
        match self.action:
            case 'resend_confirmation_mail' | 'send_reset_password_email':
                self.serializer_class = serializers.SendEmail
        return super().get_serializer_class()

    @action(['POST'], detail=False, url_path=r'email/resend-confirmation-email')
    def resend_confirmation_email(self, request, *args, **kwargs):
        """
        An endpoint for resend confirmation email if account exists.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.data

        try:
            user = User.objects.get(email=data['email'])
        except User.DoesNotExist:
            pass
        else:
            send_confirmation_email(request, user)

        return Response(None, status=status.HTTP_204_NO_CONTENT)

    @action(
        ['GET'],
        detail=False,
        url_path=r'email/confirm/(?P<uidb64>[^/.]+)/(?P<token>[^/.]+)',
    )
    def confirm_email(self, request, uidb64, token, *args, **kwargs):
        """
        Use identifiers to validate the email confirmed by the user.
        """
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user: User = User.objects.get(email=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and confirm_email_token_generator.check_token(user, token):
            user.email_verified = True
            user.save(update_fields=['email_verified'])
            login(request, user)

            return Response(None, status.HTTP_204_NO_CONTENT)
        raise Http404('Activation link is invalid.')

    @action(['POST'], detail=False, url_path=r'password/send-reset-email')
    def send_reset_password_email(self, request, *args, **kwargs):
        """
        An endpoint for send reset email if account exists.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.data

        try:
            user = User.objects.get(email=data['email'])
        except User.DoesNotExist:
            pass
        else:
            send_reset_password_email(request, user)

        return Response(None, status=status.HTTP_204_NO_CONTENT)

    @action(
        ['PUT'],
        detail=False,
        url_path=r'password/reset/(?P<uidb64>[^/.]+)/(?P<token>[^/.]+)',
    )
    def reset_password(self, request, uidb64, token, *args, **kwargs):
        """
        An endpoint for changing account passowrd.
        """
        serializer_class = serializers.ChangePassord

        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user: User = User.objects.get(email=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and password_reset_token_generator.check_token(user, token):
            serializer = serializer_class(user, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response(None, status.HTTP_204_NO_CONTENT)
        raise Http404('Activation link is invalid.')

from django.contrib.auth import authenticate, login, logout
from django.http import Http404
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from . import serializers
from .models import User
from .utils import TokenGenerator


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
    verify_email=extend_schema(
        deprecated=True,
        summary='Verify user email',
        request=None,
        responses={
            status.HTTP_200_OK: serializers.Validated,
            status.HTTP_404_NOT_FOUND: None,
        },
        tags=['authentication'],
    ),
)
class AuthViewSet(GenericViewSet):
    """Viewset with services to authentication and user session control"""

    serializer_class = serializers.User

    @action(['POST'], detail=False)
    def sign_in(self, request):
        """Sign user in session."""
        serializer = serializers.UserIn(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(**serializer.data)
        if user is not None:
            login(request, user)
            if not serializer.data.get('remember_me'):
                request.session.set_expiry(0)
            serializer = self.serializer_class(user, context={"request": request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response('User not found.', status=status.HTTP_404_NOT_FOUND)

    @action(['POST'], detail=False)
    def sign_out(self, request):
        """Sign user out in session."""
        logout(request)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(['POST'], detail=False)
    def sign_up(self, request):
        """Sign user up in DB."""
        serializer = serializers.UserUp(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.create(serializer.validated_data)  # Will use .create_user
        data = self.serializer_class(user, context={'request': request}).data

        return Response(data, status=status.HTTP_201_CREATED)

    @action(
        ['POST'],
        detail=False,
        url_path=r'verify/(?P<uidb64>[^/.]+)/(?P<token>[^/.]+)',
    )
    def verify_email(self, request, uidb64, token, *args, **kwargs):
        """Use identifiers to validate the email confirmed by the user."""
        # FIXME: create a serilizer for "uidb64" and token
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user: User = User.objects.get(email=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        token_generator = TokenGenerator()
        if user is not None and token_generator.check_token(user, token):
            user.email_verified = True
            user.save(update_fields=['email_verified'])
            data = serializers.Validated(user).data
            return Response(data, status=status.HTTP_200_OK)
        raise Http404('Activation link is invalid.')

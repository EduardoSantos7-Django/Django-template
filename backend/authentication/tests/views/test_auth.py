from django.contrib.auth import get_user
from django.contrib.auth.models import AnonymousUser
from django.core import mail
from rest_framework import status
from rest_framework.test import APITestCase

from authentication import models, views

view = views.AuthViewSet(basename='auth', request=None)


class SignUp(APITestCase):
    url = view.reverse_action(view.sign_up.url_name)

    def test_user_can_sign_up(self):
        """
        Ensure user can sign up with correct imput form data.
        """

        data = {
            'first_name': 'foo',
            'last_name': 'qux',
            'email': 'example@example.com',
            'password': 'supersecret',
            'password2': 'supersecret',
            'agreement': True,
        }
        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_cannot_sign_up_with_all_blank_fields(self):
        """
        Ensure user can't sign up if leave any field blank.
        """

        data = {}
        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_cannot_sign_up_with_mismatch_password(self):
        """
        Ensure user can't sign up when mismatch passwords.
        """

        data = {
            'first_name': 'foo',
            'last_name': 'qux',
            'email': 'example@example.com',
            'password': 'supersecret',
            'password2': 'littlesecret',
            'agreement': False,
        }
        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_when_sign_up_email_twice(self):
        """
        Ensure user can't sign up when email is already in use.
        """

        data = {
            'first_name': 'foo',
            'last_name': 'qux',
            'email': 'example@example.com',
            'password': 'supersecret',
            'password2': 'supersecret',
            'agreement': True,
        }
        for _ in range(2):
            response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class SingIn(APITestCase):
    fixtures = ['user']

    url = view.reverse_action(view.sign_in.url_name)

    def test_user_can_sign_in(self):
        """
        Ensure user can sign in.
        """

        data = {
            'email': 'foo@example.com',
            'password': 'supersecret',
        }
        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_cannot_sign_in_before_sign_up(self):
        """
        Ensure user can't sign in before creating a account.
        """

        data = {
            'email': 'no.register@example.com',
            'password': 'supersecret',
        }
        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_cannot_sign_in_with_wrong_creds(self):
        """
        Ensure user can't sign in with wrong creds.
        """

        data = {
            'email': 'foo@example.com',
            'password': 'littlesecret',  # Correct is 'supersecret'
        }
        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_when_user_sign_in_with_unverified_email(self):
        """
        Ensure user cannot sign in before verify your email.
        """

        data = {
            'email': 'example@example.com',
            'password': 'supersecret',
        }
        models.User.objects.create(
            first_name='foo', last_name='qux', email_verified=False, **data
        )

        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class SignOut(APITestCase):
    fixtures = ['user']
    url = view.reverse_action(view.sign_out.url_name)

    def setUp(self) -> None:
        """Start tests with a logged user."""
        user = models.User.objects.first()
        self.client.force_login(user)
        self.assertEqual(get_user(self.client), user)

    def test_user_can_sign_out(self):
        """
        Ensure that the user was definitely removed from session.
        """

        response = self.client.post(self.url)

        self.assertIsInstance(get_user(self.client), AnonymousUser)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

from authentication import models, views
from django.core import mail
from rest_framework import status
from rest_framework.test import APITestCase

view = views.AuthTokenViewset(basename='token', request=None)


class ConfirmEmail(APITestCase):
    def setUp(self) -> None:
        """
        Create a new user using sign_up view.
        """
        data = {
            "first_name": "First",
            "last_name": "Last",
            "email": "test@example.com",
            "password": "supersecret",
            "password2": "supersecret",
            "agreement": True,
        }

        self.client.post('/account/sign-up/', data)

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Please, confirm your email')

        self.body = mail.outbox[0].body
        *_, self.uidb64, self.token = self.body.split('/')

    def test_user_can_confirm_email(self):
        """
        Ensure user can confirm your email.
        """
        response = self.client.get(self.body)

        user = models.User.objects.get()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertTrue(user.email_verified)

    def test_user_cannot_confirm_email_twice(self):
        """
        Ensure user can't confirm your account twice in row.
        """
        for _ in range(2):
            response = self.client.get(self.body)

        user = models.User.objects.get()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(user.email_verified)

    def test_user_cannot_use_a_random_token(self):
        """
        Ensure user can't randomize your token.
        """
        random_token = self.body.replace(self.token, 'random')

        response = self.client.get(random_token)

        user = models.User.objects.get()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertFalse(user.email_verified)

    def test_user_cannot_use_a_random_uidb64(self):
        """
        Ensure user can't randomize your uidb64.
        """
        random_uidb64 = self.body.replace(self.uidb64, 'random')

        response = self.client.get(random_uidb64)

        user = models.User.objects.get()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertFalse(user.email_verified)


class ResetPassword(APITestCase):
    def setUp(self) -> None:
        """
        Create a new user using sign_up view.
        """

        self.user = models.User.objects.create_user(
            first_name="First",
            last_name="Last",
            email="test@example.com",
            email_verified=True,
            password="supersecret",
        )

        url = view.reverse_action(view.send_reset_password_email.url_name)
        data = {'email': self.user.email}
        response = self.client.post(url, data)

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Please, reset your password')

        self.body = mail.outbox[0].body
        *_, self.uidb64, self.token = self.body.split('/')

    def test_user_can_reset_password(self):
        """
        Ensure user can reset your password.
        """
        data = {
            "password": "new.password",
            "password2": "new.password",
        }
        response = self.client.put(self.body, data)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertTrue(
            self.client.login(email=self.user.email, password='new.password')
        )

    def test_user_cannot_reset_password_twice(self):
        """
        Ensure user can't reset your password twice in row.
        """
        data = {
            "password": "new.password",
            "password2": "new.password",
        }
        for _ in range(2):
            response = self.client.put(self.body, data)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(
            self.client.login(email=self.user.email, password='new.password')
        )

    def test_user_cannot_use_a_random_token(self):
        """
        Ensure user can't randomize your token.
        """
        random_token = self.body.replace(self.token, 'random')

        data = {
            "password": "new.password",
            "password2": "new.password",
        }
        response = self.client.put(random_token, data)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertFalse(
            self.client.login(email=self.user.email, password='new.password')
        )

    def test_user_cannot_use_a_random_uidb64(self):
        """
        Ensure user can't randomize your uidb64.
        """
        random_uidb64 = self.body.replace(self.uidb64, 'random')

        data = {
            "password": "new.password",
            "password2": "new.password",
        }
        response = self.client.put(random_uidb64, data)

        user = models.User.objects.get()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertFalse(
            self.client.login(email=self.user.email, password='new.password')
        )

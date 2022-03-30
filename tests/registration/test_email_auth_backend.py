# coding=utf-8
from django.contrib.auth import authenticate
from django.test import modify_settings, override_settings, TestCase
from django.urls import reverse

from tests.factories import UserFactory


class EmailAsUsernameModelBackendTestCases(TestCase):
    userdata = {
        "email": "username@example.com",
        "username": "username",
        "password": "password",
    }

    login_url = reverse("auth_login")

    def setUp(self):
        self.user = UserFactory.create(**self.userdata)


class BackendTestCases(EmailAsUsernameModelBackendTestCases):
    @override_settings(
        AUTHENTICATION_BACKENDS=["accounts.auth.EmailAsUsernameModelBackend"]
    )
    def test_only_EmailAsUsernameModelBackend(self):
        authenticated_user = authenticate(
            username="username@example.com", password="password"
        )
        assert authenticated_user == self.user

        unauthenticated_user = authenticate(username="username", password="password")
        assert unauthenticated_user is None

    @modify_settings(
        AUTHENTICATION_BACKENDS={
            "prepend": "accounts.auth.EmailAsUsernameModelBackend",
        }
    )
    def test_prepended_EmailAsUsernameModelBackend(self):
        authenticated_user = authenticate(
            username="username@example.com", password="password"
        )
        assert authenticated_user == self.user

        authenticated_user_by_usernamme = authenticate(
            username="username", password="password"
        )
        assert authenticated_user_by_usernamme == self.user

    @modify_settings(
        AUTHENTICATION_BACKENDS={
            "append": "accounts.auth.EmailAsUsernameModelBackend",
        }
    )
    def test_appended_EmailAsUsernameModelBackend(self):
        authenticated_user = authenticate(
            username="username@example.com", password="password"
        )
        assert authenticated_user == self.user

        authenticated_user_by_usernamme = authenticate(
            username="username", password="password"
        )
        assert authenticated_user_by_usernamme == self.user


class LoginViewTestCase(EmailAsUsernameModelBackendTestCases):
    def test_login_with_username(self):
        form_data = {"username": "username", "password": "password"}
        response = self.client.post(self.login_url, form_data, follow=True)

        assert response.context["user"] == self.user
        assert response.context["user"].is_authenticated is True

    def test_login_with_email_address(self):
        form_data = {"username": "username@example.com", "password": "password"}
        response = self.client.post(self.login_url, form_data, follow=True)

        assert response.context["user"] == self.user
        assert response.context["user"].is_authenticated is True

    def test_login_with_email_address_with_wrong_password(self):
        form_data = {"username": "username@example.com", "password": "wrong password"}
        response = self.client.post(self.login_url, form_data, follow=True)

        assert response.context["user"] != self.user
        assert response.context["user"].is_anonymous is True
        assert response.context["user"].is_authenticated is False

    def test_login_with_email_address_user_does_not_exist(self):
        form_data = {"username": "username2@example.com", "password": "password"}
        response = self.client.post(self.login_url, form_data, follow=True)

        assert response.context["user"] != self.user
        assert response.context["user"].is_anonymous is True
        assert response.context["user"].is_authenticated is False

    def test_login_with_email_address_duplicate_users(self):

        UserFactory.create(
            email="duplicate@example.com",
            username="duplicate_email1",
            password="password",
        )

        UserFactory.create(
            email="duplicate@example.com",
            username="duplicate_email2",
            password="password",
        )

        form_data = {"username": "duplicate@example.com", "password": "password"}
        response = self.client.post(self.login_url, form_data, follow=True)

        assert response.context["user"].is_anonymous is True
        assert response.context["user"].is_authenticated is False

    def test_login_with_email_address_with_disabled_account(self):

        self.user.is_active = False
        self.user.save()

        form_data = {"username": "username@example.com", "password": "password"}
        response = self.client.post(self.login_url, form_data, follow=True)

        assert response.context["user"] != self.user
        assert response.context["user"].is_anonymous is True
        assert response.context["user"].is_authenticated is False

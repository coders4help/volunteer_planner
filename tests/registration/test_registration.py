# coding=utf-8
import pytest

from django.test import TestCase, override_settings
from django.urls import reverse

from registration.models import RegistrationProfile

from accounts.models import UserAccount


@override_settings(LANGUAGE_CODE="en", LANGUAGES=(("en", "English"),))
class RegistrationTestCase(TestCase):
    def setUp(self):
        # TODO: fix typo in url name in urls.py
        self.registration_url = reverse("registration_register")

        self.valid_user_data = {
            "username": "somename",
            "email": "somename@example.de",
            "password1": "somepassword",
            "password2": "somepassword",
            "accept_privacy_policy": True,
        }

    def test_get_displays_empty_form(self):
        response = self.client.get(self.registration_url)
        assert response.status_code == 200
        self.assertTemplateUsed(response, "registration/registration_form.html")

        form = response.context["form"]
        assert form is not None

        initial_data = form.initial
        assert len(initial_data) == 0

    def test_submit_empty_form(self):
        # shall not raise an exception
        response = self.client.post(self.registration_url, {})

        form = response.context["form"]
        assert form is not None, "We expect the form to be displayed again if the submission failed"

        self.assertFormError(response, "form", "email", "This field is required.")

        assert RegistrationProfile.objects.count() == 0

    def test_invalid_email(self):
        user_data = {
            "username": "somename",
            "email": "invalid-address",
            "password1": "somepassword",
            "password2": "differentpassword",
        }

        response = self.client.post(self.registration_url, user_data)

        form = response.context["form"]
        assert form is not None, "We expect the form to be displayed again if the submission failed"

        # TODO: implement form error and then assertFormError
        # see for example test_username_exists_already

        assert RegistrationProfile.objects.count() == 0

    def try_invalid_username(self, invalid_username):
        """
        helper method for the next couple of tests checking invalid usernames
        """
        user_data = {
            "username": invalid_username,
            "email": "somename@example.de",
            "password1": "somepassword",
            "password2": "somepassword",
        }

        response = self.client.post(self.registration_url, user_data)

        form = response.context["form"]
        assert form is not None, "We expect the form to be displayed again if the submission failed"

        self.assertFormError(
            response,
            "form",
            "username",
            "Enter a valid username. This value may contain only letters, numbers, and @/./+/-/_ characters.",
        )

        assert RegistrationProfile.objects.count() == 0

    def test_username_with_whitespaces(self):
        self.try_invalid_username("some invalid name")

    def test_username_with_special_chars(self):
        self.try_invalid_username("someinvalidname$")

    def test_username_with_umlauts(self):
        self.try_invalid_username("somename with ÖÄÜäöüß")

    def test_username_exists_already(self):
        # register first user
        self.client.post(self.registration_url, self.valid_user_data)

        # try to register user again (=same username)
        response = self.client.post(self.registration_url, self.valid_user_data)

        form = response.context["form"]
        assert form is not None, "We expect the form to be displayed again if the submission failed"

        self.assertFormError(response, "form", "username", "A user with that username already exists.")

        assert RegistrationProfile.objects.count() == 1

    def test_passwords_dont_match(self):
        user_data = {
            "username": "somename",
            "email": "somename@example.de",
            "password1": "somepassword",
            "password2": "differentpassword",
        }

        response = self.client.post(self.registration_url, user_data)

        form = response.context["form"]
        assert form is not None, "We expect the form to be displayed again if the submission failed"

        # TODO: why is this a non-field error? Shouldn't it be a error on the
        # second password field?
        self.assertFormError(response, "form", "password2", "The two password fields didn’t match.")

        assert RegistrationProfile.objects.count() == 0

    def test_submit_valid_form(self):
        response = self.client.post(self.registration_url, self.valid_user_data, follow=True)

        registration_complete_url = reverse("registration_complete")

        self.assertRedirects(response, registration_complete_url)
        self.assertContains(response, "An activation mail will be sent to you email address.")

        assert RegistrationProfile.objects.count() == 1
        new_user = RegistrationProfile.objects.first()
        assert new_user is not None
        assert new_user.user.username == "somename"

    def test_registered_user_is_inactive(self):
        self.client.post(self.registration_url, self.valid_user_data)

        new_user = RegistrationProfile.objects.first()
        assert not new_user.user.is_active

        with pytest.raises(UserAccount.DoesNotExist):
            UserAccount.objects.get(user=new_user.user)

    def test_activate_registered_user(self):
        self.client.post(self.registration_url, self.valid_user_data)

        new_user = RegistrationProfile.objects.first()

        assert not new_user.user.is_active

        activation_key = new_user.activation_key
        activation_url = reverse(
            "registration_activate",
            args=[
                activation_key,
            ],
        )

        response = self.client.get(activation_url, follow=True)

        activation_complete_url = reverse("registration_activation_complete")

        self.assertRedirects(response, activation_complete_url)

        user_from_regprofile = RegistrationProfile.objects.get(user=new_user.user).user
        user_from_account = UserAccount.objects.get(user=new_user.user).user

        assert user_from_account == user_from_regprofile
        assert user_from_account.is_active
        assert user_from_regprofile.is_active

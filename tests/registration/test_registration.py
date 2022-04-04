# coding=utf-8
import pytest
from django.test import override_settings, TestCase
from django.urls import reverse
from registration.models import RegistrationProfile

from accounts.forms import RegistrationForm
from accounts.models import UserAccount


@pytest.mark.django_db
@pytest.mark.parametrize(
    "username",
    [
        "jusernäym",
        "üser.name",
        "user.name2",
        "user.name2_",
        "username_2",
        "username_2",
        "ÄBCDEF0123456789",
    ],
)
def test_submit_valid_username(username):
    formdata = {
        "username": username,
        "email": "somename@example.com",
        "password1": "somepassword",
        "password2": "somepassword",
        "accept_privacy_policy": True,
    }
    form = RegistrationForm(formdata)
    assert not form.errors
    assert form.is_valid()


@override_settings(LANGUAGE_CODE="en", LANGUAGES=(("en", "English"),))
class RegistrationTestCase(TestCase):
    def setUp(self):
        self.registration_url = reverse("registration_register")

        self.valid_user_data = {
            "username": "Some.name123_",
            "email": "somename@example.com",
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
        assert (
            form is not None
        ), "We expect the form to be displayed again if the submission failed"

        self.assertFormError(response, "form", "email", "This field is required.")

        assert RegistrationProfile.objects.count() == 0

    def test_invalid_email(self):
        user_data = {
            "username": "somename",
            "email": "invalid-address",
            "password1": "somepassword",
            "password2": "differentpassword",
            "accept_privacy_policy": True,
        }

        response = self.client.post(self.registration_url, user_data)

        form = response.context["form"]
        assert (
            form is not None
        ), "We expect the form to be displayed again if the submission failed"

        # TODO: implement form error and then assertFormError
        # see for example test_username_exists_already

        assert RegistrationProfile.objects.count() == 0

    def try_invalid_username(self, invalid_username, expected_errors):
        """
        helper method for the next couple of tests checking invalid usernames
        """
        user_data = {
            "username": invalid_username,
            "email": "somename@example.com",
            "password1": "somepassword",
            "password2": "somepassword",
            "accept_privacy_policy": True,
        }

        response = self.client.post(self.registration_url, user_data)

        form = response.context["form"]
        assert form is not None, "Form not displayed again after submission failed"

        self.assertFormError(
            response,
            "form",
            "username",
            expected_errors,
        )

        assert RegistrationProfile.objects.count() == 0

    def test_username_beginning(self):
        self.try_invalid_username("1username", "Username must start with a letter.")
        self.try_invalid_username(".username", "Username must start with a letter.")
        self.try_invalid_username("_username", "Username must start with a letter.")

    def test_username_ending(self):
        self.try_invalid_username(
            "username.", 'Username must end with a letter, a number or "_".'
        )

    def test_username_too_short(self):
        self.try_invalid_username(
            "ab", "Ensure this value has at least 3 characters (it has 2)."
        )

    def test_username_too_long(self):
        self.try_invalid_username(
            "abcdef0123456789.abcdef0123456789",
            "Ensure this value has at most 32 characters (it has 33).",
        )

    def test_username_with_consequtive_underscores(self):
        self.try_invalid_username(
            "invalid__name",
            'Username must not contain consecutive "." or "_" characters.',
        )

        self.try_invalid_username(
            "invalid___name",
            'Username must not contain consecutive "." or "_" characters.',
        )

    def test_username_with_consequtive_dots(self):
        self.try_invalid_username(
            "invalid..name",
            'Username must not contain consecutive "." or "_" characters.',
        )
        self.try_invalid_username(
            "invalid...name",
            'Username must not contain consecutive "." or "_" characters.',
        )

    def test_username_with_consequtive_funnystuff(self):
        self.try_invalid_username(
            "invalid._._name",
            'Username must not contain consecutive "." or "_" characters.',
        )
        self.try_invalid_username(
            "invalid_._name",
            'Username must not contain consecutive "." or "_" characters.',
        )

    def test_username_with_whitespaces(self):
        self.try_invalid_username(
            "user name",
            "Invalid username. "
            'Allowed characters are letters, numbers, "." and "_".',
        )
        self.try_invalid_username(
            " username",
            [
                "Invalid username. "
                'Allowed characters are letters, numbers, "." and "_".',
            ],
        )
        self.try_invalid_username(
            "username ",
            [
                'Username must end with a letter, a number or "_".',
                "Invalid username. "
                'Allowed characters are letters, numbers, "." and "_".',
            ],
        )
        self.try_invalid_username(
            " username ",
            [
                'Username must end with a letter, a number or "_".',
                "Invalid username. "
                'Allowed characters are letters, numbers, "." and "_".',
            ],
        )
        self.try_invalid_username(
            " user name ",
            [
                'Username must end with a letter, a number or "_".',
                "Invalid username. "
                'Allowed characters are letters, numbers, "." and "_".',
            ],
        )

    def test_username_with_special_chars(self):
        self.try_invalid_username(
            "invalidname$",
            'Invalid username. Allowed characters are letters, numbers, "." and "_".',
        )
        self.try_invalid_username(
            "emoji_😀name",
            'Invalid username. Allowed characters are letters, numbers, "." and "_".',
        )

    def test_username_exists_already(self):
        # register first user
        self.client.post(self.registration_url, self.valid_user_data)

        # try to register user again (=same username)
        response = self.client.post(self.registration_url, self.valid_user_data)

        form = response.context["form"]
        assert (
            form is not None
        ), "We expect the form to be displayed again if the submission failed"

        self.assertFormError(
            response, "form", "username", "A user with that username already exists."
        )

        assert RegistrationProfile.objects.count() == 1

    def test_privacy_policy_missing(self):
        user_data = {
            "username": "somename",
            "email": "somename@example.com",
            "password1": "somepassword",
            "password2": "somepassword",
            # "accept_privacy_policy": True,
        }

        response = self.client.post(self.registration_url, user_data, follow=True)

        form = response.context["form"]
        assert (
            form is not None
        ), "We expect the form to be displayed again if the submission failed"

        self.assertFormError(
            response, "form", "accept_privacy_policy", "This field is required."
        )

        assert RegistrationProfile.objects.count() == 0

    def test_privacy_policy_not_accepted(self):
        user_data = {
            "username": "somename",
            "email": "somename@example.com",
            "password1": "somepassword",
            "password2": "somepassword",
            "accept_privacy_policy": "false",
        }

        response = self.client.post(self.registration_url, user_data, follow=True)

        assert RegistrationProfile.objects.count() == 0

        form = response.context["form"]
        assert (
            form is not None
        ), "We expect the form to be displayed again if the submission failed"

        self.assertFormError(
            response, "form", "accept_privacy_policy", "This field is required."
        )

    def test_passwords_dont_match(self):
        user_data = {
            "username": "somename",
            "email": "somename@example.com",
            "password1": "somepassword",
            "password2": "differentpassword",
            "accept_privacy_policy": True,
        }

        response = self.client.post(self.registration_url, user_data, follow=True)

        assert RegistrationProfile.objects.count() == 0

        form = response.context["form"]
        assert (
            form is not None
        ), "We expect the form to be displayed again if the submission failed"

        # TODO: why is this a non-field error? Shouldn't it be a error on the
        # second password field?
        self.assertFormError(
            response, "form", "password2", "The two password fields didn’t match."
        )

    def test_registered_user_is_inactive(self):
        self.client.post(self.registration_url, self.valid_user_data)

        new_user = RegistrationProfile.objects.first()
        assert new_user is not None
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

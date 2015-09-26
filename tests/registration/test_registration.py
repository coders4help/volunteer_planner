from django.test import TestCase
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from registration.models import RegistrationProfile


class RegistrationTestCase(TestCase):

    def setUp(self):
        # TODO: fix typo in url name in urls.py
        self.registration_url = reverse('registation')

        self.valid_user_data = {'username': 'somename',
                                'email': 'somename@example.de',
                                'password1': 'somepassword',
                                'password2': 'somepassword'}

    def test_get_displays_empty_form(self):
        response = self.client.get(self.registration_url)
        assert response.status_code == 200
        self.assertTemplateUsed(response, 'registration_form.html')

        form = response.context['form']
        assert form is not None

        initial_data = form.initial
        assert len(initial_data) == 0

    def test_submit_empty_form(self):
        # shall not raise an exception
        response = self.client.post(self.registration_url, {})

        form = response.context['form']
        assert form is not None, 'We expect the form to be displayed again if the submission failed'

        self.assertFormError(
            response,
            'form',
            'email',
            'Dieses Feld ist zwingend erforderlich.')

        assert RegistrationProfile.objects.count() == 0

    def test_invalid_email(self):
        user_data = {'username': 'somename',
                     'email': 'invalid-address',
                     'password1': 'somepassword',
                     'password2': 'differentpassword'}

        response = self.client.post(self.registration_url, user_data)

        form = response.context['form']
        assert form is not None, 'We expect the form to be displayed again if the submission failed'

        # TODO: implement form error and then assertFormError
        # see for example test_username_exists_already

        assert RegistrationProfile.objects.count() == 0

    def try_invalid_username(self, invalid_username):
        """
        helper method for the next couple of tests checking invalid usernames
        """
        user_data = {'username': invalid_username,
                     'email': 'somename@example.de',
                     'password1': 'somepassword',
                     'password2': 'somepassword'}

        response = self.client.post(self.registration_url, user_data)

        form = response.context['form']
        assert form is not None, 'We expect the form to be displayed again if the submission failed'

        self.assertFormError(
            response,
            'form',
            'username',
            _(u'This value may contain only letters, numbers and @/./+/-/_ characters.'))

        assert RegistrationProfile.objects.count() == 0

    def test_username_with_whitespaces(self):
        self.try_invalid_username('some invalid name')

    def test_username_with_special_chars(self):
        self.try_invalid_username('someinvalidname$')

    def test_username_with_umlauts(self):
        self.try_invalid_username(unicode('somename\xc3', errors='replace'))

    def test_username_exists_already(self):
        # register first user
        self.client.post(self.registration_url, self.valid_user_data)

        # try to register user again (=same username)
        response = self.client.post(self.registration_url,
                                    self.valid_user_data)

        form = response.context['form']
        assert form is not None, 'We expect the form to be displayed again if the submission failed'

        self.assertFormError(
            response,
            'form',
            'username',
            _(u'A user with that username already exists.'))

        assert RegistrationProfile.objects.count() == 1

    def test_passwords_dont_match(self):
        user_data = {'username': 'somename',
                     'email': 'somename@example.de',
                     'password1': 'somepassword',
                     'password2': 'differentpassword'}

        response = self.client.post(self.registration_url, user_data)

        form = response.context['form']
        assert form is not None, 'We expect the form to be displayed again if the submission failed'

        # TODO: why is this a non-field error? Shouldn't it be a error on the
        # second password field?
        self.assertFormError(
            response,
            'form',
            None,
            'Die zwei Passwoerter sind nicht gleich!')

        assert RegistrationProfile.objects.count() == 0

    def test_submit_valid_form(self):
        response = self.client.post(self.registration_url,
                                    self.valid_user_data,
                                    follow=True)

        registration_complete_url = reverse('registration_complete')

        self.assertRedirects(response, registration_complete_url)
        self.assertContains(
            response, 'Eine Aktivierungsmail wurde Dir soeben zugesendet.')

        assert RegistrationProfile.objects.count() == 1
        new_user = RegistrationProfile.objects.first()
        assert new_user is not None
        assert new_user.user.username == "somename"

    def test_registered_user_is_inactive(self):
        self.client.post(self.registration_url, self.valid_user_data)

        new_user = RegistrationProfile.objects.first()
        assert not new_user.user.is_active

    def test_activate_registered_user(self):
        self.client.post(self.registration_url, self.valid_user_data)

        new_user = RegistrationProfile.objects.first()

        assert not new_user.user.is_active

        activation_url = reverse('user_activate')
        activation_key = new_user.activation_key

        response = self.client.get(activation_url,
                                   data={'activation_key': activation_key},
                                   follow=True)

        activation_complete_url = reverse('registration_activation_complete')

        self.assertRedirects(response, activation_complete_url)

        assert RegistrationProfile.objects.first().user.is_active

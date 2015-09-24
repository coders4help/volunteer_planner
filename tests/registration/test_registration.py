from django.test import TestCase
from django.core.urlresolvers import reverse


from registration.models import RegistrationProfile


class RegistrationTestCase(TestCase):

    valid_user_data = {'username': 'somename',
                       'email': 'somename@example.de',
                       'password1': 'somepassword',
                       'password2': 'somepassword'}

    def test_get_displays_empty_form(self):
        # TODO: fix typo in url name in urls.py
        registration_url = reverse('registation')

        response = self.client.get(registration_url)
        assert response.status_code == 200
        self.assertTemplateUsed(response, 'registration_form.html')

        form = response.context['form']
        assert form is not None

        initial_data = form.initial
        assert len(initial_data) == 0

    def test_submit_empty_form(self):
        # TODO: fix typo in url name in urls.py
        registration_url = reverse('registation')

        # shall not raise an exception
        response = self.client.post(registration_url, {})

        assert RegistrationProfile.objects.count() == 0

        form = response.context['form']
        assert form is not None, 'We expect the form to be displayed again if the submission failed'

        self.assertFormError(
            response,
            'form',
            'email',
            'Dieses Feld ist zwingend erforderlich.')

    def test_submit_valid_form(self):
        # TODO: fix typo in url name in urls.py
        registration_url = reverse('registation')

        response = self.client.post(registration_url,
                                    self.valid_user_data,
                                    follow=True)

        registration_complete_url = reverse('registration_complete')

        self.assertRedirects(response, registration_complete_url)
        self.assertContains(
            response, 'Eine Aktivierungsmail wurde Dir soeben zugesendet.')

        new_user = RegistrationProfile.objects.first()
        assert new_user is not None
        assert new_user.user.username == "somename"

    def test_username_exists_already(self):
        # TODO: fix typo in url name in urls.py
        registration_url = reverse('registation')

        # register first user
        self.client.post(registration_url, self.valid_user_data)

        # try to register user again (=same username)
        response = self.client.post(registration_url,
                                    self.valid_user_data)

        assert RegistrationProfile.objects.count() == 1

        form = response.context['form']
        assert form is not None, 'We expect the form to be displayed again if the submission failed'

        self.assertFormError(
            response,
            'form',
            'username',
            'Dieser Benutzername ist bereits vergeben.')

    def test_passwords_dont_match(self):
        # TODO: fix typo in url name in urls.py
        registration_url = reverse('registation')

        user_data = {'username': 'somename',
                     'email': 'somename@example.de',
                     'password1': 'somepassword',
                     'password2': 'differentpassword'}

        response = self.client.post(registration_url, user_data)

        assert RegistrationProfile.objects.count() == 0

        form = response.context['form']
        assert form is not None, 'We expect the form to be displayed again if the submission failed'

        # TODO: why is this a non-field error? Shouldn't it be a error on the
        # second password field?
        self.assertFormError(
            response,
            'form',
            None,
            'Die zwei Passwoerter sind nicht gleich!')

    def try_invalid_username(self, invalid_username):
        """
        helper method for the next couple of tests checking invalid usernames
        """
        # TODO: fix typo in url name in urls.py
        registration_url = reverse('registation')

        user_data = {'username': invalid_username,
                     'email': 'somename@example.de',
                     'password1': 'somepassword',
                     'password2': 'somepassword'}

        response = self.client.post(registration_url, user_data)

        assert RegistrationProfile.objects.count() == 0

        form = response.context['form']
        assert form is not None, 'We expect the form to be displayed again if the submission failed'

        self.assertFormError(
            response,
            'form',
            'username',
            'This value may contain only letters, numbers and @/./+/-/_ characters.')

    def test_username_with_whitespaces(self):
        self.try_invalid_username('some invalid name')

    def test_username_with_special_chars(self):
        self.try_invalid_username('someinvalidname$')

    def test_username_with_umlauts(self):
        self.try_invalid_username(unicode('somename\xc3', errors='replace'))

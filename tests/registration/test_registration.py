from django.test import TestCase
from django.core.urlresolvers import reverse


from registration.models import RegistrationProfile


class RegistrationTestCase(TestCase):

    def test_get_displays_empty_form(self):
        # TODO: fix typo in url name in urls.py
        registration_url = reverse('registation')

        response = self.client.get(registration_url)
        assert response.status_code == 200

        form = response.context['form']
        assert form is not None

        initial_data = form.initial
        assert len(initial_data) == 0

    def test_submit_empty_form(self):
        # TODO: fix typo in url name in urls.py
        registration_url = reverse('registation')

        # shall not raise an exception
        response = self.client.post(registration_url, {})

        form = response.context['form']
        assert form is not None, "We expect the form to be displayed again if the submission failed"

        self.assertContains(response, 'Dieses Feld ist zwingend erforderlich.')

    def test_submit_valid_form(self):
        # TODO: fix typo in url name in urls.py
        registration_url = reverse('registation')

        response = self.client.post(registration_url,
                                    {'username': 'somename',
                                     'email': 'myaddress@example.com',
                                     'password1': 'somepassword',
                                     'password2': 'somepassword'},
                                    follow=True)

        assert response.status_code == 200
        self.assertContains(
            response, 'Eine Aktivierungsmail wurde Dir soeben zugesendet.')

        new_user = RegistrationProfile.objects.first()
        assert new_user is not None
        assert new_user.user.username == "somename"

from django.test import TestCase
from django.core.urlresolvers import reverse


class RegistrationTestCase(TestCase):

    def test_get_displays_empty_form(self):
        registration_url = reverse('registation')  # TODO: fix typo in url name in urls.py

        response = self.client.get(registration_url)
        assert response.status_code == 200

        form = response.context['form']
        assert form is not None

        initial_data = form.initial
        assert len(initial_data) == 0

    def test_submit_empty_form(self):
        registration_url = reverse('registation')  # TODO: fix typo in url name in urls.py
        response = self.client.post(registration_url, {})  # shall not raise an exception

        self.assertContains(response, 'Dieses Feld ist zwingend erforderlich.')

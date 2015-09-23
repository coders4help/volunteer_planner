from django.test import TestCase
from django.core.urlresolvers import reverse


class RegistrationTestCase(TestCase):

    def test_displays_empty_form(self):
        registration_url = reverse('registation')  # TODO: fix typo in url name in urls.py

        response = self.client.get(registration_url)
        form = response.context['form']

        assert form is not None

        initial_data = form.initial
        assert len(initial_data) == 0

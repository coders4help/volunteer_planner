import pytest

from django.core import management


@pytest.mark.django_db
def test_create_dummy_data():
    """
    Tests that the create_dummy_data management command runs through. It's important
    for local development.
    """
    management.call_command('create_dummy_data', '1')

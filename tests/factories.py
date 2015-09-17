# coding: utf-8
import string

import factory
from django.contrib.auth.models import User
from factory.fuzzy import FuzzyText
from scheduler import models as scheduler_models
from registration import models as registration_models


class TopicFactory(factory.DjangoModelFactory):
    class Meta:
        model = scheduler_models.Topics
        django_get_or_create = ['title']

    description = FuzzyText(length=150, chars=string.ascii_letters, prefix='')


class LocationFactory(factory.DjangoModelFactory):
    class Meta:
        model = scheduler_models.Location
        django_get_or_create = ['name']




class NeedFactory(factory.DjangoModelFactory):
    class Meta:
        model = scheduler_models.Need

    topic = factory.SubFactory(TopicFactory)
    location = factory.SubFactory(LocationFactory)

    slots = 10


class UserFactory(factory.DjangoModelFactory):
    class Meta:
        model = User

    username = FuzzyText(length=10, chars=string.ascii_letters, prefix='')
    first_name = FuzzyText(length=10, chars=string.ascii_letters, prefix='')
    last_name = FuzzyText(length=10, chars=string.ascii_letters, prefix='')
    password = factory.PostGenerationMethodCall('set_password',
                                                'defaultpassword')
    email = factory.LazyAttribute(lambda o: '%s@example.com' % o.last_name)


class RegistrationProfileFactory(factory.DjangoModelFactory):
    class Meta:
        model = registration_models.RegistrationProfile

    user = factory.SubFactory(UserFactory)
    activation_key = "ACTIVATION_KEY"



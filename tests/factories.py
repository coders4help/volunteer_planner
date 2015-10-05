# coding: utf-8
import string

import factory
from django.contrib.auth.models import User
from factory.fuzzy import FuzzyText

from accounts import models as account_models

from scheduler import models as scheduler_models
from places import models as places_models


class TopicFactory(factory.DjangoModelFactory):
    title = "Sample topic"

    class Meta:
        model = scheduler_models.Topics
        django_get_or_create = ['title']

    description = FuzzyText(length=150, chars=string.ascii_letters, prefix='')


class CountryFactory(factory.DjangoModelFactory):
    class Meta:
        model = places_models.Country

    name = factory.Sequence(lambda n: 'Country ' + str(n))
    slug = factory.Sequence(lambda n: 'country_' + str(n))


class RegionFactory(factory.DjangoModelFactory):
    class Meta:
        model = places_models.Region

    name = factory.Sequence(lambda n: 'Region ' + str(n))
    slug = factory.Sequence(lambda n: 'region_' + str(n))

    country = factory.SubFactory(CountryFactory)


class AreaFactory(factory.DjangoModelFactory):
    class Meta:
        model = places_models.Area

    name = factory.Sequence(lambda n: 'Area ' + str(n))
    slug = factory.Sequence(lambda n: 'area_' + str(n))

    region = factory.SubFactory(RegionFactory)


class PlaceFactory(factory.DjangoModelFactory):
    class Meta:
        model = places_models.Place

    name = factory.Sequence(lambda n: 'Place ' + str(n))
    slug = factory.Sequence(lambda n: 'place_' + str(n))

    area = factory.SubFactory(AreaFactory)


class LocationFactory(factory.DjangoModelFactory):
    name = "Rathaus W"
    place = factory.SubFactory(PlaceFactory)

    class Meta:
        model = scheduler_models.Location
        django_get_or_create = ['name', 'place']


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


class UserAccountFactory(factory.DjangoModelFactory):
    class Meta:
        model = account_models.UserAccount

    user = factory.SubFactory(UserFactory)

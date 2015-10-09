# coding: utf-8
import string

import factory
from django.contrib.auth.models import User
from factory.fuzzy import FuzzyText

from accounts import models as account_models
from scheduler import models as scheduler_models
from places import models as places_models
from organizations import models as organization_models


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


class OrganizationFactory(factory.DjangoModelFactory):
    name = "Rathaus W"

    class Meta:
        model = organization_models.Organization
        django_get_or_create = ['name', ]


class FacilityFactory(factory.DjangoModelFactory):
    name = "Rathaus W"
    place = factory.SubFactory(PlaceFactory)
    organization = factory.SubFactory(OrganizationFactory)

    class Meta:
        model = organization_models.Facility
        django_get_or_create = ['name', 'place', 'organization']


class TaskFactory(factory.DjangoModelFactory):
    class Meta:
        model = organization_models.Task

    name = "Küchenhilfe"
    description = "Teller waschen"
    facility = factory.SubFactory(FacilityFactory)


class ShiftFactory(factory.DjangoModelFactory):
    class Meta:
        model = scheduler_models.Shift

    task = factory.SubFactory(TaskFactory)
    facility = factory.SubFactory(FacilityFactory)

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


class ShiftHelperFactory(factory.DjangoModelFactory):
    class Meta:
        model = scheduler_models.ShiftHelper
        django_get_or_create = ['shift']

    user_account = factory.SubFactory(UserAccountFactory)

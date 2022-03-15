# coding: utf-8
import string
from datetime import datetime


from django.contrib.auth.models import User

from factory import Sequence, SubFactory, LazyAttribute, PostGenerationMethodCall
from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyText

from accounts import models as account_models
from scheduler import models as scheduler_models
from places import models as places_models
from organizations import models as organization_models


class CountryFactory(DjangoModelFactory):
    class Meta:
        model = places_models.Country

    name = Sequence(lambda n: 'Country ' + str(n))
    slug = Sequence(lambda n: 'country_' + str(n))


class RegionFactory(DjangoModelFactory):
    class Meta:
        model = places_models.Region

    name = Sequence(lambda n: 'Region ' + str(n))
    slug = Sequence(lambda n: 'region_' + str(n))

    country = SubFactory(CountryFactory)


class AreaFactory(DjangoModelFactory):
    class Meta:
        model = places_models.Area

    name = Sequence(lambda n: 'Area ' + str(n))
    slug = Sequence(lambda n: 'area_' + str(n))

    region = SubFactory(RegionFactory)


class PlaceFactory(DjangoModelFactory):
    class Meta:
        model = places_models.Place

    name = Sequence(lambda n: 'Place ' + str(n))
    slug = Sequence(lambda n: 'place_' + str(n))

    area = SubFactory(AreaFactory)


class OrganizationFactory(DjangoModelFactory):
    name = Sequence(lambda n: 'Organization ' + str(n))
    slug = Sequence(lambda n: 'org_' + str(n))

    class Meta:
        model = organization_models.Organization
        django_get_or_create = ['name']


class FacilityFactory(DjangoModelFactory):
    name = Sequence(lambda n: 'Facility ' + str(n))
    slug = Sequence(lambda n: 'facility_' + str(n))

    place = SubFactory(PlaceFactory)
    organization = SubFactory(OrganizationFactory)

    class Meta:
        model = organization_models.Facility
        django_get_or_create = ['name', 'place', 'organization']


class TaskFactory(DjangoModelFactory):
    class Meta:
        model = organization_models.Task

    name = Sequence(lambda n: 'Task ' + str(n))
    description = Sequence(lambda n: 'task ' + str(n))

    facility = SubFactory(FacilityFactory)


class ShiftFactory(DjangoModelFactory):
    class Meta:
        model = scheduler_models.Shift

    task = SubFactory(TaskFactory)
    facility = SubFactory(FacilityFactory)

    starting_time = datetime(2016, 2, 13, 19, 0)
    ending_time = datetime(2016, 2, 13, 20, 0)
    slots = 10


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    username = FuzzyText(length=10, chars=string.ascii_letters, prefix='')
    first_name = FuzzyText(length=10, chars=string.ascii_letters, prefix='')
    last_name = FuzzyText(length=10, chars=string.ascii_letters, prefix='')
    password = PostGenerationMethodCall('set_password', 'defaultpassword')
    email = LazyAttribute(lambda o: '%s@example.com' % o.last_name)


class UserAccountFactory(DjangoModelFactory):
    class Meta:
        model = account_models.UserAccount

    user = SubFactory(UserFactory)


class ShiftHelperFactory(DjangoModelFactory):
    class Meta:
        model = scheduler_models.ShiftHelper
        django_get_or_create = ['shift']

    user_account = SubFactory(UserAccountFactory)
    shift = SubFactory(ShiftFactory)

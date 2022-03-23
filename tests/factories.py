# coding: utf-8
import string
from datetime import datetime, timedelta

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

    name = Sequence(lambda n: f"Country {n}")
    slug = Sequence(lambda n: f"country_{n}")


class RegionFactory(DjangoModelFactory):
    class Meta:
        model = places_models.Region

    name = Sequence(lambda n: f"Region {n}")
    slug = Sequence(lambda n: f"region_{n}")

    country = SubFactory(CountryFactory)


class AreaFactory(DjangoModelFactory):
    class Meta:
        model = places_models.Area

    name = Sequence(lambda n: f"Area {n}")
    slug = Sequence(lambda n: f"area_{n}")

    region = SubFactory(RegionFactory)


class PlaceFactory(DjangoModelFactory):
    class Meta:
        model = places_models.Place

    name = Sequence(lambda n: f"Place {n}")
    slug = Sequence(lambda n: f"place_{n}")

    area = SubFactory(AreaFactory)


class OrganizationFactory(DjangoModelFactory):
    name = Sequence(lambda n: f"Organization {n}")
    slug = Sequence(lambda n: f"org_{n}")

    class Meta:
        model = organization_models.Organization
        django_get_or_create = ["name"]


class FacilityFactory(DjangoModelFactory):
    name = Sequence(lambda n: f"Facility {n}")
    slug = Sequence(lambda n: f"facility_{n}")

    place = SubFactory(PlaceFactory)
    organization = SubFactory(OrganizationFactory)

    class Meta:
        model = organization_models.Facility
        django_get_or_create = ["name", "place", "organization"]


class TaskFactory(DjangoModelFactory):
    class Meta:
        model = organization_models.Task

    name = Sequence(lambda n: f"Task {n}")
    description = Sequence(lambda n: f"task {n}")

    facility = SubFactory(FacilityFactory)


class WorkplaceFactory(DjangoModelFactory):
    class Meta:
        model = organization_models.Workplace

    name = Sequence(lambda n: f"Workplace {n}")
    description = Sequence(lambda n: f"workplace {n}")

    facility = SubFactory(FacilityFactory)


class ShiftFactory(DjangoModelFactory):
    class Meta:
        model = scheduler_models.Shift

    task = SubFactory(TaskFactory)
    facility = SubFactory(FacilityFactory)
    workplace = SubFactory(WorkplaceFactory)

    starting_time = datetime.now() + timedelta(
        hours=0.5
    )  # create a shift in the future, so test users can subscribe
    ending_time = starting_time + timedelta(
        hours=1
    )  # let shift end one hour after it started
    slots = 10


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    username = FuzzyText(length=10, chars=string.ascii_letters, prefix="")
    first_name = FuzzyText(length=10, chars=string.ascii_letters, prefix="")
    last_name = FuzzyText(length=10, chars=string.ascii_letters, prefix="")
    password = PostGenerationMethodCall("set_password", "defaultpassword")
    email = LazyAttribute(lambda o: f"{o.last_name}@example.com")


class UserAccountFactory(DjangoModelFactory):
    class Meta:
        model = account_models.UserAccount

    user = SubFactory(UserFactory)


class ShiftHelperFactory(DjangoModelFactory):
    class Meta:
        model = scheduler_models.ShiftHelper
        django_get_or_create = ["shift"]

    user_account = SubFactory(UserAccountFactory)
    shift = SubFactory(ShiftFactory)

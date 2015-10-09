# coding: utf-8

from datetime import timedelta

from django.db import models
from django.utils import timezone

from places import models as place_models
from organizations import models as organization_models


class ShiftManager(models.Manager):
    def at_facility(self, facility):
        return self.get_queryset().filter(facility=facility)

    def at_place(self, place):
        return self.get_queryset().filter(facility__place=place)

    def in_area(self, area):
        return self.get_queryset().filter(facility__place__area=area)

    def in_region(self, region):
        return self.get_queryset().filter(facility__place__area__region=region)

    def in_country(self, country):
        return self.get_queryset().filter(
            facility__place__area__region__country=country)

    def by_geography(self, geo_affiliation):
        if isinstance(geo_affiliation, organization_models.Facility):
            return self.at_facility(geo_affiliation)
        elif isinstance(geo_affiliation, place_models.Place):
            return self.at_place(geo_affiliation)
        elif isinstance(geo_affiliation, place_models.Area):
            return self.in_area(geo_affiliation)
        elif isinstance(geo_affiliation, place_models.Region):
            return self.in_region(geo_affiliation)
        elif isinstance(geo_affiliation, place_models.Country):
            return self.in_country(geo_affiliation)


class OpenShiftManager(ShiftManager):
    def get_queryset(self):
        now = timezone.now()
        qs = super(OpenShiftManager, self).get_queryset()
        return qs.filter(ending_time__gte=now)


class ShiftHelperManager(models.Manager):
    def conflicting(self, shift, user_account=None, grace=timedelta(hours=1)):

        grace = grace or timedelta(0)
        graced_start = shift.starting_time + grace
        graced_end = shift.ending_time - grace

        query_set = self.get_queryset().select_related('shift', 'user_account')

        if user_account:
            query_set = query_set.filter(user_account=user_account)

        query_set = query_set.exclude(shift__starting_time__lt=graced_start,
                                      shift__ending_time__lte=graced_start)
        query_set = query_set.exclude(shift__starting_time__gte=graced_end,
                                      shift__ending_time__gte=graced_end)
        return query_set

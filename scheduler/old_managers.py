# coding: utf-8
from datetime import timedelta
from django.db import models
from django.utils import timezone
from organizations.models import Facility
from places.models import Place, Area, Region, Country


class NeedManager(models.Manager):
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
        if isinstance(geo_affiliation, Facility):
            return self.at_facility(geo_affiliation)
        elif isinstance(geo_affiliation, Place):
            return self.at_place(geo_affiliation)
        elif isinstance(geo_affiliation, Area):
            return self.in_area(geo_affiliation)
        elif isinstance(geo_affiliation, Region):
            return self.in_region(geo_affiliation)
        elif isinstance(geo_affiliation, Country):
            return self.in_country(geo_affiliation)


class OpenNeedManager(NeedManager):
    def get_queryset(self):
        now = timezone.now()
        qs = super(OpenNeedManager, self).get_queryset()
        return qs.filter(ending_time__gte=now)


class ShiftHelperManager(models.Manager):
    def conflicting(self, need, user_account=None, grace=timedelta(hours=1)):

        grace = grace or timedelta(0)
        graced_start = need.starting_time + grace
        graced_end = need.ending_time - grace

        query_set = self.get_queryset().select_related('need', 'user_account')

        if user_account:
            query_set = query_set.filter(user_account=user_account)

        query_set = query_set.exclude(need__starting_time__lt=graced_start,
                                      need__ending_time__lte=graced_start)
        query_set = query_set.exclude(need__starting_time__gte=graced_end,
                                      need__ending_time__gte=graced_end)
        return query_set

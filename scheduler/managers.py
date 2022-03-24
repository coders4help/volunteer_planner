# coding: utf-8

from datetime import datetime, time, timedelta

from django.db import models
from django.utils import timezone
from django.conf import settings

from places import models as place_models


class ShiftQuerySet(models.QuerySet):
    """ Custom QuerySet for Shift. Defines several methods for filtering
        Shift objects.
    """
    def on_shiftdate(self, shiftdate):
        """ Shifts that end on or after shiftdate and begin before or on
            shiftdate. That means shifts that intersect with the day of
            shiftdate.
        """
        # make sure, shiftdate is a date and not a datetime
        shiftdate = datetime.combine(shiftdate, time.min).date()
        return self.filter(ending_time__gte=shiftdate,
                           starting_time__lt=shiftdate + timedelta(days=1))

    def at_place(self, place):
        """ Shifts at a certain place (geographical location of a facility).
        See places.models.
        """
        return self.filter(facility__place=place)

    def in_area(self, area):
        """ Shifts at a certain area (subdivision of a region).
        See places.models.
        """
        return self.filter(facility__place__area=area)

    def in_region(self, region):
        """ Shifts at a certain region. See places.models.
        """
        return self.filter(facility__place__area__region=region)

    def in_country(self, country):
        """ Shifts at a certain country. See places.models.
        """
        return self.filter(
            facility__place__area__region__country=country)

    def by_geography(self, geo_affiliation):
        """ Shifts at a certain geo_affiliation which can be a place, area,
            region or country. See places.models.
        """
        if isinstance(geo_affiliation, place_models.Place):
            return self.at_place(geo_affiliation)
        elif isinstance(geo_affiliation, place_models.Area):
            return self.in_area(geo_affiliation)
        elif isinstance(geo_affiliation, place_models.Region):
            return self.in_region(geo_affiliation)
        elif isinstance(geo_affiliation, place_models.Country):
            return self.in_country(geo_affiliation)

# Create manager from custom QuerySet ShiftQuerySet
ShiftManager = models.Manager.from_queryset(ShiftQuerySet)


class OpenShiftManager(ShiftManager):
    """ Manager for Shift. Overwrites get_queryset with a filter on QuerySet
        that holds all shifts that end now or in the future.
    """
    def get_queryset(self):
        now = timezone.now()
        qs = super(OpenShiftManager, self).get_queryset()
        return qs.filter(ending_time__gte=now)


class ShiftHelperManager(models.Manager):
    """ Manager for ShiftHelper. Defines one method for filtering the
        QuerySet on conflicting shifts.
    """

    def conflicting(self, shift, user_account=None, grace=settings.DEFAULT_SHIFT_CONFLICT_GRACE):
        """ Filters QuerySet of ShiftHelper objects by selecting those that
            intersect with respect to time.

            :param shift
            :param user_account - default is None (-Does a default value for
                    user make sense in that connection?)
            :param grace - some "buffer" which reduces the time of the shift.
                    default is 1 hour
        """
        grace = grace or timedelta(0)

        # correct grace for short shifts, otherwise a user could join two concurrent 1-hour-shifts
        if shift.duration <= grace:
            grace = shift.duration / 2
        graced_start = shift.starting_time + grace
        graced_end = shift.ending_time - grace

        query_set = self.get_queryset().select_related('shift', 'user_account')

        if user_account:
            query_set = query_set.filter(user_account=user_account)

        soft_conflict_query_set = query_set.exclude(shift__starting_time__lt=shift.starting_time,
                                                    shift__ending_time__lte=shift.starting_time)
        soft_conflict_query_set = soft_conflict_query_set.exclude(shift__starting_time__gte=shift.ending_time,
                                                                  shift__ending_time__gte=shift.ending_time)

        hard_conflict_query_set = query_set.exclude(shift__starting_time__lt=graced_start,
                                                    shift__ending_time__lte=graced_start)
        hard_conflict_query_set = hard_conflict_query_set.exclude(shift__starting_time__gte=graced_end,
                                                                  shift__ending_time__gte=graced_end)

        return hard_conflict_query_set, soft_conflict_query_set

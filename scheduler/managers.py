# coding: utf-8

from datetime import timedelta

from django.db import models

from django.utils import timezone

from organizations.models import Facility
from places.models import Place, Area, Region, Country


class EnrolmentManager(models.Manager):
    def conflicting(self, shift, user_account=None, grace=timedelta(hours=1)):

        grace = grace or timedelta(0)
        graced_start = shift.starting_time + grace
        graced_end = shift.ending_time - grace

        query_set = self.get_queryset().select_related('shift', 'user_account')

        if user_account:
            query_set = query_set.filter(user=user_account)

        query_set = query_set.exclude(shift__start_time__lt=graced_start,
                                      shift__end_time__lte=graced_start)
        query_set = query_set.exclude(shift__start_time__gte=graced_end,
                                      shift__end_time__gte=graced_end)
        return query_set


# This "second" view allows to create/publish the shifts for the X coming days out of the
# recurring events.
# On REST side, it should be possible to request all events from the template for a specified day,
# return them to the front-end which will publish them and/or modify them via PUTs statements


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


class ShiftManager(NeedManager):
    """
    Draft of what blueprinting methods could look like. But there's no need for
    them to live in a manager. Better to have a dedicated blueprinting module,
    or such like.

    def create_datetime_from_day_and_time_string(self, day, time_str):
        return parse(time_str, default=day)

    def create_shift_from_event_and_day(self, event, day):
        shift = Shift(task=event.task,
                      workplace=event.workplace,
                      name=event.name,
                      description=event.description,
                      slot_amount=event.slot_amount,
                      start_time=self.create_datetime_from_day_and_time_string(day, event.start_time),
                      end_time=self.create_datetime_from_day_and_time_string(day, event.end_time))
        # shift.save() # see if it should be done here later
        return shift

    def create_shifts_for_facility_and_day(self, facility, day):
        events = RecurringEvent.objects.get_events_for_facility_and_day(facility, day)
        shifts = []
        for event in events:
            shifts.append(self.create_shift_from_event_and_day(event, day))
        return shifts
    """

    def open_shifts(self):
        return super(ShiftManager, self).get_queryset().filter(
            end_time__gte=timezone.now())


class RecurringEventManager(models.Manager):
    def get_events_for_facility_and_day(self, facility, day):
        weekday = day.weekday()
        # since working with datetime, we may need to add timedelta and so here
        return self.filter(facility=facility,
                           weekday=weekday,
                           first_date__gte=day,
                           end_date__lte=day,
                           disabled=False)


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

# coding: utf-8

from datetime import timedelta

from django.db import models

from django.utils import timezone

from scheduler.old_managers import NeedManager


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




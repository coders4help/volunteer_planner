import os

from django.conf import settings
from django.core.management.base import BaseCommand
import datetime
from registration.models import RegistrationProfile

from stats.models import ValueStore


class Command(BaseCommand):
    help = 'creates bulk shifts from existing data'
    args = ""

    option_list = BaseCommand.option_list

    def handle(self, *args, **options):
        shifts = RegistrationProfile.objects.all()\
            .filter(needs__time_period_from__date_time__lte=datetime.datetime.now())
        seconds = 0.0
        for shift in shifts:
            theshift = shift.needs.all()
            for single_shift in theshift:
                deelta = single_shift.time_period_to.date_time - single_shift.time_period_from.date_time
                seconds += deelta.total_seconds()
        total_hours = int(((seconds/60)/60))
        try:
            key = ValueStore.objects.get(name="total-volunteer-hours")
            key.value = total_hours
            key.save()
        except ValueStore.DoesNotExist:
            ValueStore.objects.create(name="total-volunteer-hours", value=total_hours)






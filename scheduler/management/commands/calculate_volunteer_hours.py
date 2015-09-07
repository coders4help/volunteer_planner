import os

from django.conf import settings
from django.core.management.base import BaseCommand
import datetime
from registration.models import RegistrationProfile


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
        print int(((seconds/60)/60))

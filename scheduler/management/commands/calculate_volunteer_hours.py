# coding: utf-8

import datetime

from django.core.management.base import BaseCommand

from registration.models import RegistrationProfile
from stats.models import ValueStore


class Command(BaseCommand):
    help = 'creates bulk shifts from existing data'
    args = ""

    option_list = BaseCommand.option_list

    def handle(self, *args, **options):
        shifts = RegistrationProfile.objects.all()\
            .filter(needs__time_period_from__date_time__lte=datetime.datetime.now())\
            .prefetch_related('needs', 'needs__time_period_to', 'needs__time_period_from')\
            .only('needs__time_period_to', 'needs__time_period_from')

        total_seconds = 0.0
        for shift in shifts:
            needs_in_shift = shift.needs.all()
            for single_shift in needs_in_shift:
                delta = single_shift.time_period_to.date_time - single_shift.time_period_from.date_time
                total_seconds += delta.total_seconds()
        total_hours = int(total_seconds)/3600

        value_object, created = ValueStore.objects.get_or_create(name="total-volunteer-hours", defaults=dict(value=total_hours))
        if not created:
            value_object.value = total_hours
            value_object.save()

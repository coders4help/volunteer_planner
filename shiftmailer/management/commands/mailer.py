# coding: utf-8

import datetime

from django.core.management.base import BaseCommand

from django.template.loader import render_to_string
from django.db.models import Count

from scheduler.models import Need
from shiftmailer.models import Mailer
from shiftmailer.excelexport import GenerateExcelSheet


class Command(BaseCommand):
    help = 'sends emails taken from addresses (.models.mailer) with a list of shifts for this day' \
           'run my cronjob'
    args = ""

    def handle(self, *args, **options):
        mailer = Mailer.objects.all()
        for mail in mailer:
            now = datetime.datetime.now()
            needs = Need.objects.filter(location=mail.location).filter(
                ending_time__year=now.strftime("%Y"),
                ending_time__month=now.strftime("%m"),
                ending_time__day=now.strftime("%d")) \
                .order_by('topic', 'ending_time') \
                .annotate(volunteer_count=Count('registrationprofile')) \
                .select_related('topic', 'location') \
                .prefetch_related('registrationprofile_set', 'registrationprofile_set__user')

            message = render_to_string('shifts_today.html', locals())
            iua = GenerateExcelSheet(needs=needs, mailer=mail)

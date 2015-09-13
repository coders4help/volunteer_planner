# coding: utf-8

import datetime

from django.core.management.base import BaseCommand

from django.template.loader import render_to_string

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
            needs = Need.objects.filter(location=mail.location). \
                filter(
                time_period_to__date_time__year=now.strftime("%Y"),
                time_period_to__date_time__month=now.strftime("%m"),
                time_period_to__date_time__day=now.strftime("%d")) \
                .order_by('topic', 'time_period_to__date_time')

            message = render_to_string('shifts_today.html', locals())
            iua = GenerateExcelSheet(needs=needs, mailer=mail)

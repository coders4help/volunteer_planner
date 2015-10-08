# coding: utf-8

import datetime

from django.core.management.base import BaseCommand

# from django.template.loader import render_to_string
from django.db.models import Count

from scheduler.models import Shift
from shiftmailer.models import Mailer
from shiftmailer.excelexport import GenerateExcelSheet

DATE_FORMAT = '%d.%m.%Y'


class Command(BaseCommand):
    help = 'sends emails taken from addresses (.models.mailer) with a list of shifts for this day' \
           'run my cronjob'

    def add_arguments(self, parser):
        parser.add_argument('--date', dest='print_date', default=datetime.date.today().strftime(DATE_FORMAT),
                            help='The date to generate scheduler for')

    def handle(self, *args, **options):
        mailer = Mailer.objects.all()
        t = datetime.datetime.strptime(options['print_date'], DATE_FORMAT)
        for mail in mailer:
            shifts = Shift.objects.filter(facility=mail.facility).filter(
                ending_time__year=t.strftime("%Y"),
                ending_time__month=t.strftime("%m"),
                ending_time__day=t.strftime("%d")) \
                .order_by('topic', 'ending_time') \
                .annotate(volunteer_count=Count('helpers')) \
                .select_related('topic', 'facility') \
                .prefetch_related('helpers', 'helpers__user')
            # if it's not used anyway, we maybe shouldn't even render it? #
            # message = render_to_string('shifts_today.html', locals())
            iua = GenerateExcelSheet(shifts=shifts, mailer=mail)
            iua.send_file()

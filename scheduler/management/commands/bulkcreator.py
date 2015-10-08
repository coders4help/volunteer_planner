# coding: utf-8

from datetime import timedelta

from django.core.management.base import BaseCommand
from dateutil.parser import parse

from organizations.models import Facility
from scheduler.models import Topics, Shift


class Command(BaseCommand):
    help = 'creates bulk shifts from existing data'
    args = ""

    option_list = BaseCommand.option_list

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('date', nargs='+', type=int)

    def handle(self, *args, **options):
        if options['days_to_add'] and options['facility_id']:
            print options['days_to_add']
            print options['facility_id']

            facility = Facility.objects.get(id=options['facility_id'][0])
            facility_shifts = facility.shift_set.all()
            topic_titles = []
            for shift in facility_shifts:
                if shift.topic.title not in topic_titles:
                    topic_titles.append(shift.topic.title)

            for topic_title in topic_titles:
                topic = Topics.objects.filter(title=topic_title)[:1]
                topic_shifts = Shift.objects.filter(topic__title=topic_title)

                for shift in topic_shifts:
                    date_new_to = parse(str(shift.ending_time))
                    date_new_from = parse(str(shift.starting_time))

                    for i in range(int(options['days_to_add'][0])):
                        ending_time = date_new_to + timedelta(days=i)
                        starting_time = date_new_from + timedelta(days=i)

                        Shift.objects.create(topic=topic[0],
                                             facility=facility,
                                             slots=shift.slots,
                                             starting_time=starting_time,
                                             ending_time=ending_time)

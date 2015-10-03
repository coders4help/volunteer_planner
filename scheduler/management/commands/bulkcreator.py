# coding: utf-8

from datetime import timedelta

from django.core.management.base import BaseCommand
from dateutil.parser import parse

from organizations.models import Facility
from scheduler.models import Need, Topics


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
            facility_needs = facility.need_set.all()
            topic_titles = []
            for need in facility_needs:
                if need.topic.title not in topic_titles:
                    topic_titles.append(need.topic.title)

            for topic_title in topic_titles:
                topic = Topics.objects.filter(title=topic_title)[:1]
                topic_needs = Need.objects.filter(topic__title=topic_title)

                for need in topic_needs:
                    date_new_to = parse(str(need.ending_time))
                    date_new_from = parse(str(need.starting_time))

                    for i in range(int(options['days_to_add'][0])):
                        ending_time = date_new_to + timedelta(days=i)
                        starting_time = date_new_from + timedelta(days=i)

                        Need.objects.create(topic=topic[0],
                                            facility=facility,
                                            slots=need.slots,
                                            starting_time=starting_time,
                                            ending_time=ending_time)

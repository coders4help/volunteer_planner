import os

from django.conf import settings
from django.core.management.base import BaseCommand
import datetime
from datetime import date, timedelta
from scheduler.models import Need, Location, Topics, TimePeriods
from dateutil.parser import *
import ipdb


class Command(BaseCommand):
    help = 'creates bulk shifts from existing data'
    args = ""

    option_list = BaseCommand.option_list

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('date', nargs='+', type=int)

    def handle(self, *args, **options):
        if options['days_to_add'] and options['location_id']:
            print options['days_to_add']
            print options['location_id']

            location = Location.objects.get(id=options['location_id'][0])
            needs = location.need_set.all()
            topic_titles = []
            for need in needs:
                if need.topic.title not in topic_titles:
                    topic_titles.append(need.topic.title)

            for item in topic_titles:
                topic = Topics.objects.filter(title=item)[:1]
                needs_needs = Need.objects.filter(topic__title=item)
                for needy in needs_needs:
                    to_time = str(needy.time_period_to)
                    from_time = str(needy.time_period_from)
                    date_new_to = parse(to_time)
                    date_new_from = parse(from_time)

                    for i in range(int(options['days_to_add'][0])):
                        newtime_to = date_new_to + datetime.timedelta(days=i)
                        newtime_from = date_new_from + datetime.timedelta(days=i)
                        from_the_time = TimePeriods(date_time=newtime_from)
                        from_the_time.save()
                        to_the_time = TimePeriods(date_time=newtime_to)
                        to_the_time.save()
                        new_row = Need(topic=topic[0])
                        new_row.location = location
                        new_row.slots = needy.slots

                        new_row.time_period_to = to_the_time
                        new_row.time_period_from = from_the_time
                        new_row.save()
                        # ipdb.set_trace()

                    # newtime = date_new +datetime.timedelta(days=1)
                    # ipdb.set_trace()
                    # print newtime
                    # print date.today() + timedelta(days=1)
                # Need(location=location, topic=topic)
            # ipdb.set_trace()

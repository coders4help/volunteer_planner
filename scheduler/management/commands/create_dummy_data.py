# coding: utf-8

import random
import string
import datetime
import factory
from django.core.management.base import BaseCommand
from django.db.models import signals
from tests.factories import NeedFactory, TopicFactory, LocationFactory, RegistrationProfileFactory
from registration.models import RegistrationProfile
from scheduler.models import Need, Location, Topics
from django.contrib.auth.models import User

HELPTOPICS = ["Jumper", "Translator", "Clothing Room", "Womens Room", "Donation Counter", "Highlights" ]
LOREM = "Lorem tellivizzle dolizzle bling bling amizzle, mah nizzle adipiscing" \
        " elit. Nullam doggy velizzle, pizzle volutpizzle, suscipizzle" \
        " quizzle, gangsta vizzle, i'm in the shizzle. Pellentesque boom" \
        " shackalack for sure. The bizzle erizzle. Fusce izzle dolor " \
        "dapibus shit tempizzle dang. Sure pellentesque nibh izzle turpis." \
        " Vestibulum izzle tortor. Pellentesque ma nizzle rhoncizzle " \
        "bling bling. In hizzle habitasse i'm in the shizzle dictumst. " \
        "Bizzle dapibizzle. Curabitizzle tellizzle urna, pretizzle i" \
        " saw beyonces tizzles and my pizzle went crizzle, " \
        "mattis we gonna chung, eleifend vitae, nunc. "


class Command(BaseCommand):
    help = 'this command creates dummy data for the entire ' \
           'application execute \"python manage.py create_dummy_data 30 --flush True\"' \
           'to first delete all data in the database and then ad random shifts for 30 days.' \
           'if you don\'t want to delete data just not add \"flush True\"   '

    args = ""

    option_list = BaseCommand.option_list

    def add_arguments(self, parser):
        parser.add_argument('days', nargs='+', type=int)
        parser.add_argument('--flush')

    def gen_date(self, hour, day):
        date_today = datetime.date.today() + datetime.timedelta(days=day)
        date_time = datetime.time(hour=hour, minute=0, second=0, microsecond=0)
        new_date = datetime.datetime.combine(date_today, date_time)
        return new_date

    def random_string(self, length=10):
        return u''.join(random.choice(string.ascii_letters) for x in range(length))

    @factory.django.mute_signals(signals.pre_delete)
    def handle(self, *args, **options):
        if options['flush']:
            print "delete all data in app tables"
            RegistrationProfile.objects.all().delete()
            Need.objects.all().delete()
            Location.objects.all().delete()
            Topics.objects.all().delete()
            User.objects.filter().exclude(is_superuser=True).delete()

        # create shifts for number of days
        for day in range(0, options['days'][0]):
            for i in range(2, 23):
                topic = TopicFactory.create(title=random.choice(HELPTOPICS))
                location = LocationFactory.create(name="Shelter" + str(random.randint(0,9)), additional_info=LOREM)
                need = NeedFactory.create(
                    starting_time=self.gen_date(hour=i-1, day=day),
                    ending_time=self.gen_date(hour=i, day=day),
                    topic=topic,
                    location=location
                )
                # assign random volunteer for each need
                reg_user = RegistrationProfileFactory.create()
                reg_user.needs.add(need)
                reg_user.save()






















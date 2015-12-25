# coding: utf-8

import random
import string
import datetime

import factory
from django.core.management.base import BaseCommand
from django.db.models import signals
from registration.models import RegistrationProfile

from django.contrib.auth.models import User
from accounts.models import UserAccount

from organizations.models import Facility, Workplace, Task
from tests.factories import ShiftHelperFactory, ShiftFactory, FacilityFactory, PlaceFactory, OrganizationFactory
from scheduler.models import Shift
from places.models import Region, Area, Place, Country

HELPTOPICS = ["Jumper", "Translator", "Clothing Room", "Womens Room",
              "Donation Counter", "Highlights"]
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


def gen_date(hour, day):
    date_today = datetime.date.today() + datetime.timedelta(days=day)
    date_time = datetime.time(hour=hour, minute=0, second=0, microsecond=0)
    new_date = datetime.datetime.combine(date_today, date_time)
    return new_date


def random_string(length=10):
    return u''.join(
        random.choice(string.ascii_letters) for x in range(length))


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

    @factory.django.mute_signals(signals.pre_delete)
    def handle(self, *args, **options):
        if options['flush']:
            print "delete all data in app tables"
            RegistrationProfile.objects.all().delete()

            Shift.objects.all().delete()
            Task.objects.all().delete()
            Workplace.objects.all().delete()
            Facility.objects.all().delete()

            UserAccount.objects.all().delete()

            # delete geographic information
            Country.objects.all().delete()
            Region.objects.all().delete()
            Area.objects.all().delete()
            Place.objects.all().delete()

            User.objects.filter().exclude(is_superuser=True).delete()

        # create regional data
        places = list()
        for i in range(0, 10):
            places.append(PlaceFactory.create())

        organizations = list()
        for i in range(0, 4):
            organizations.append(OrganizationFactory.create())

        # create shifts for number of days
        for day in range(0, options['days'][0]):
            for i in range(2, 23):
                place = places[random.randint(0, len(places) - 1)]
                organization = organizations[random.randint(0, len(organizations) - 1)]
                facility = FacilityFactory.create(
                    description=LOREM,
                    place=place,
                    organization=organization
                )
                shift = ShiftFactory.create(
                    starting_time=gen_date(hour=i - 1, day=day),
                    ending_time=gen_date(hour=i, day=day),
                    facility=facility
                )
                # assign random volunteer for each shift
                reg_user = ShiftHelperFactory.create(shift=shift)
                reg_user.save()

# coding: utf-8

import random
import string
import datetime

import factory
from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.models import signals
from registration.models import RegistrationProfile

from django.contrib.auth.models import User
from accounts.models import UserAccount

from organizations.models import Facility, Workplace, Task, Organization
from tests.factories import (
    ShiftHelperFactory,
    ShiftFactory,
    FacilityFactory,
    PlaceFactory,
    OrganizationFactory,
    TaskFactory,
    WorkplaceFactory,
    UserFactory,
    UserAccountFactory,
)
from scheduler.models import Shift, ShiftHelper
from places.models import Region, Area, Place, Country

HELPTOPICS = [
    "Jumper",
    "Translator",
    "Clothing Room",
    "Womens Room",
    "Donation Counter",
    "Highlights",
]
LOREM = (
    "Lorem tellivizzle dolizzle bling bling amizzle, mah nizzle adipiscing"
    " elit. Nullam doggy velizzle, pizzle volutpizzle, suscipizzle"
    " quizzle, gangsta vizzle, i'm in the shizzle. Pellentesque boom"
    " shackalack for sure. The bizzle erizzle. Fusce izzle dolor "
    "dapibus shit tempizzle dang. Sure pellentesque nibh izzle turpis."
    " Vestibulum izzle tortor. Pellentesque ma nizzle rhoncizzle "
    "bling bling. In hizzle habitasse i'm in the shizzle dictumst. "
    "Bizzle dapibizzle. Curabitizzle tellizzle urna, pretizzle i"
    " saw beyonces tizzles and my pizzle went crizzle, "
    "mattis we gonna chung, eleifend vitae, nunc. "
)


def gen_date(hour, day):
    date_today = datetime.date.today() + datetime.timedelta(days=day)
    date_time = datetime.time(hour=hour, minute=0, second=0, microsecond=0)
    new_date = datetime.datetime.combine(date_today, date_time)
    return new_date


def random_string(length=10):
    return "".join(random.choice(string.ascii_letters) for x in range(length))


class Command(BaseCommand):
    help = (
        "this command creates dummy data for the entire "
        'application execute "python manage.py create_dummy_data 30 --flush True"'
        "to first delete all data in the database and then ad random shifts for 30 days."
        'if you don\'t want to delete data just not add "flush True"   '
    )

    args = ""

    def add_arguments(self, parser):
        parser.add_argument("days", nargs="+", type=int)
        parser.add_argument("--flush")

    @factory.django.mute_signals(signals.pre_delete)
    def handle(self, *args, **options):
        with transaction.atomic():
            if options["flush"]:
                print("delete all data in app tables")
                for model in (
                    RegistrationProfile,
                    ShiftHelper,
                    Shift,
                    UserAccount,
                    Task,
                    Workplace,
                    Facility,
                    Organization,
                    Place,
                    Area,
                    Region,
                    Country,
                ):
                    model.objects.all().delete()
                User.objects.filter().exclude(is_superuser=True).delete()

            print("creating new dummy data")
            # create regional data
            places = [PlaceFactory.create() for _ in range(0, 10)]

            # create organizations and facilities
            organizations = [OrganizationFactory.create() for _ in range(0, 4)]
            facilities = [
                FacilityFactory.create(
                    description=LOREM,
                    place=random.choice(places),
                    organization=random.choice(organizations),
                )
                for _ in range(0, len(organizations) * 2)
            ]

            # create tasks and workplaces
            i = 0
            tasks = list()
            workplaces = list()
            for fac in facilities:
                tasks.extend(
                    [
                        TaskFactory.create(
                            name=f"Task {i + j}",
                            description=f"task {i + j}",
                            facility=fac,
                        )
                        for j in range(0, random.randint(1, 5))
                    ]
                )
                workplaces.extend(
                    [
                        WorkplaceFactory.create(
                            name=f"Workplace {i + j}",
                            description=f"workplace {i + j}",
                            facility=fac,
                        )
                        for j in range(0, random.randint(1, 5))
                    ]
                )
                i += 1

            # create shifts for number of days
            for day in range(0, options["days"][0]):
                for i in range(2, 23):
                    task = random.choice(tasks)
                    facility = task.facility
                    workplace = random.choice(
                        list(filter(lambda w: w.facility == facility, workplaces))
                    )
                    shift = ShiftFactory.create(
                        starting_time=gen_date(hour=i - 1, day=day),
                        ending_time=gen_date(hour=i, day=day),
                        facility=facility,
                        task=task,
                        workplace=workplace,
                    )
                    # assign random volunteer for each shift
                    reg_user = ShiftHelperFactory.create(shift=shift)

            for i in range(0, 5):
                UserAccountFactory.create(user=UserFactory.create(username=f"user{i}"))

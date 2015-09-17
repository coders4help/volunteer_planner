# coding: utf-8

import datetime
import random
import string

from django.core.management.base import BaseCommand
from django.db.models import signals
import factory
from registration.models import RegistrationProfile
from stats.models import ValueStore
from scheduler.models import Need, Location, Topics
from tests import factories


class Command(BaseCommand):
    help = 'this command creates dummy data for the entire application'
    args = ""

    option_list = BaseCommand.option_list
    def add_arguments(self, parser):
        parser.add_argument('with_flush')


    def random_string(length=10):
        return u''.join(random.choice(string.ascii_letters) for x in range(length))

    @factory.django.mute_signals(signals.pre_delete)
    def handle(self, *args, **options):
        if options['with_flush']:
            print "delete all data in app tables"
            RegistrationProfile.objects.all().delete()
            Need.objects.all().delete()
            Location.objects.all().delete()
            Topics.objects.all().delete()

        need = factories.NeedFactory()
        import ipdb
        ipdb.set_trace()

















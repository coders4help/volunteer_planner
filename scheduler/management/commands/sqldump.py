# coding=utf-8
import os

from django.conf import settings
from django.core.management.base import BaseCommand
import datetime


class Command(BaseCommand):
    help = 'dump complete database as sql'
    args = ""

    option_list = BaseCommand.option_list

    def handle(self, *fixture_labels, **options):
        db = settings.DATABASES['default']['NAME']
        user = settings.DATABASES['default']['USER']
        password = settings.DATABASES['default']['PASSWORD']
        ts = datetime.datetime.isoformat(datetime.datetime.now())

        # one to easily load and one timestamped, safe is safe!
        os.system('mysqldump -u %s --password="%s" %s | gzip > var/%s.dump.sql.gz' % (user, password, db, ts))
        os.system('ln -fs %s.dump.sql.gz var/dump.sql.gz' % ts)

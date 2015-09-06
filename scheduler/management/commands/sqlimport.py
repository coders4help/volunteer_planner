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

        # first make a dump haha!
        os.system('mysqldump -u %s --password="%s" %s | gzip > var/%s.dump.sql.gz' % (user, password, db, ts))
        # then load new sql
        os.system('gunzip < var/dump.sql.gz | mysql -u %s --password="%s" %s' % (user, password, db))

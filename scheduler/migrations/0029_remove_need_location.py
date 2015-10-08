# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('scheduler', '0028_need_facility'),
        ('organizations', '0002_migrate_locations_to_facilities')
    ]

    operations = [
        migrations.RemoveField(
            model_name='need',
            name='location',
        ),
    ]

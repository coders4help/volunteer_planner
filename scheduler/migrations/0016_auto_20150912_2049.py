# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scheduler', '0015_auto_20150912_1732'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='location',
            options={'verbose_name': 'location', 'verbose_name_plural': 'locations', 'permissions': (('can_view', 'User can view location'),)},
        ),
        migrations.AlterModelOptions(
            name='timeperiods',
            options={'verbose_name': 'timeperiod', 'verbose_name_plural': 'timeperiods'},
        ),
        migrations.AlterModelOptions(
            name='topics',
            options={'verbose_name': 'helptype', 'verbose_name_plural': 'helptypes'},
        ),
    ]

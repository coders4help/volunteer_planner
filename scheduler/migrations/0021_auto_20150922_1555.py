# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scheduler', '0020_Fix_Working_Hours'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='need',
            options={'ordering': ['starting_time', 'ending_time'], 'verbose_name': 'shift', 'verbose_name_plural': 'shifts'},
        ),
    ]

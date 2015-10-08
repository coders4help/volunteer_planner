# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scheduler', '0028_need_facility'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='need',
            name='location',
        ),
    ]

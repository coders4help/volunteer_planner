# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scheduler', '0011_auto_20150906_2341'),
    ]

    operations = [
        migrations.RenameField(
            model_name='location',
            old_name='altitude',
            new_name='latitude',
        ),
    ]

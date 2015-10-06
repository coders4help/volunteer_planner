# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0004_add_tasks'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='facility',
            name='slug',
        ),
        migrations.RemoveField(
            model_name='organization',
            name='slug',
        ),
        migrations.RemoveField(
            model_name='task',
            name='slug',
        ),
        migrations.RemoveField(
            model_name='workplace',
            name='slug',
        ),
    ]

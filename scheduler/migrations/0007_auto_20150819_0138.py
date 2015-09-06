# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scheduler', '0006_auto_20150819_0134'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='volunteers',
            name='interests',
        ),
        migrations.RemoveField(
            model_name='volunteers',
            name='needs',
        ),
        migrations.RemoveField(
            model_name='volunteers',
            name='user',
        ),
        migrations.DeleteModel(
            name='Volunteers',
        ),
    ]

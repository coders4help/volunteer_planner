# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scheduler', '0007_auto_20150819_0138'),
        ('registration', '0002_auto_20150819_0134'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='registrationprofile',
            name='interests',
        ),
        migrations.AddField(
            model_name='registrationprofile',
            name='interests',
            field=models.ManyToManyField(to='scheduler.Topics'),
        ),
    ]

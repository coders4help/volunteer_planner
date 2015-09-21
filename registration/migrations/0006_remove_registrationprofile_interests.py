# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0005_merge'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='registrationprofile',
            name='interests',
        ),
    ]

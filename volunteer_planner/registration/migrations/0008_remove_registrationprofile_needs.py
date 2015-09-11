# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0007_auto_20150910_2126'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='registrationprofile',
            name='needs',
        ),
    ]

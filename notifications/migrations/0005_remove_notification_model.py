# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0004_auto_20151003_2033'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notification',
            name='facility',
        ),
        migrations.DeleteModel(
            name='Notification',
        ),
    ]

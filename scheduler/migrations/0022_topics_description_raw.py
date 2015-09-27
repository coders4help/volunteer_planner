# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scheduler', '0021_auto_20150922_1555'),
    ]

    operations = [
        migrations.AddField(
            model_name='topics',
            name='description_raw',
            field=models.TextField(max_length=20000, blank=True),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scheduler', '0013_auto_20150912_1334'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='need',
            name='activate',
        ),
    ]

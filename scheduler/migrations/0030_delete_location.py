# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scheduler', '0029_remove_need_location'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='location',
            name='place',
        ),
        migrations.DeleteModel(
            name='Location',
        ),
    ]

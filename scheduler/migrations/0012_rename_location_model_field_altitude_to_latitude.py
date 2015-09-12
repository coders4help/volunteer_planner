# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('scheduler', '0011_auto_20150906_2341'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='location',
            options={'verbose_name': 'Ort', 'verbose_name_plural': 'Orte',
                     'permissions': (('can_view', 'User can view location'),)},
        ),
        migrations.RenameField(
            model_name='location',
            old_name='altitude',
            new_name='latitude',
        ),
    ]

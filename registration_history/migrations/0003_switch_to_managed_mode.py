# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('registration_history', '0002_move_user_needs'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='oldregistrationprofile',
            options={
                'managed': True
            },
        ),
        migrations.AlterModelOptions(
            name='oldregistrationprofileneed',
            options={
                'managed': True
            },
        ),
    ]

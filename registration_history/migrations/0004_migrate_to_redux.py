# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('registration_history', '0003_switch_to_managed_mode'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='oldregistrationprofile',
            options={
                'managed': True,
                'verbose_name': 'registration profile',
                'verbose_name_plural': 'registration profiles'
            },
        ),
        migrations.RemoveField(
            model_name='oldregistrationprofile',
            name='needs',
        ),
        migrations.DeleteModel(
            name='OldRegistrationProfileNeed',
        ),
    ]

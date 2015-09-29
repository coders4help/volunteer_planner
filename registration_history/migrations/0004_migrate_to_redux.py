# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registration_history', '0003_switch_to_managed_mode'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='oldregistrationprofileneed',
            name='need',
        ),
        migrations.RemoveField(
            model_name='oldregistrationprofileneed',
            name='registrationprofile',
        ),
        migrations.AlterModelOptions(
            name='oldregistrationprofile',
            options={'managed': True, 'verbose_name': 'registration profile', 'verbose_name_plural': 'registration profiles'},
        ),
        migrations.RemoveField(
            model_name='oldregistrationprofile',
            name='needs',
        ),
        migrations.AddField(
            model_name='oldregistrationprofile',
            name='activated',
            field=models.BooleanField(default=False),
        ),
        migrations.DeleteModel(
            name='OldRegistrationProfileNeed',
        ),
    ]

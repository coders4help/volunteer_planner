# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('registration_history', '0005_update_activated'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='oldregistrationprofile',
            options={
                'managed': False,
                'verbose_name': 'registration profile',
                'verbose_name_plural': 'registration profiles'
            },
        ),
        migrations.RemoveField(
            model_name='oldregistrationprofile',
            name='user',
        ),
        migrations.DeleteModel(
            name='OldRegistrationProfile',
        ),
    ]

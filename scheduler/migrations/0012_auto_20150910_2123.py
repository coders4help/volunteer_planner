# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0005_merge'),
        ('scheduler', '0011_auto_20150906_2341'),
    ]

    operations = [
        migrations.CreateModel(
            name='scheduledRegPro',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('did_show_up', models.BooleanField(default=False)),
                ('need', models.ForeignKey(to='scheduler.Need')),
                ('registration_profile', models.ForeignKey(to='registration.RegistrationProfile')),
            ],
        ),
        migrations.AlterModelOptions(
            name='location',
            options={'verbose_name': 'Ort', 'verbose_name_plural': 'Orte', 'permissions': (('can_view', 'User can view location'), ('can_checkin', 'Can checkin volunteers'))},
        ),
    ]

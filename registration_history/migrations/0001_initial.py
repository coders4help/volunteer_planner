# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='OldRegistrationProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('activation_key', models.CharField(max_length=40, verbose_name='activation key')),
            ],
            options={
                'db_table': 'registration_registrationprofile',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='OldRegistrationProfileNeed',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
                'db_table': 'registration_registrationprofile_needs',
                'managed': False,
            },
        ),
    ]

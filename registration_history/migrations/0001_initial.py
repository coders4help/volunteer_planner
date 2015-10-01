# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0001_initial'),
        ('scheduler', '0025_merge'),
    ]

    operations = [
        migrations.CreateModel(
            name='OldRegistrationProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False,
                                        auto_created=True, primary_key=True)),
                ('activation_key', models.CharField(max_length=40,
                                                    verbose_name='activation key')),
            ],
            options={
                'db_table': 'registration_registrationprofile',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='OldRegistrationProfileNeed',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False,
                                        auto_created=True, primary_key=True)),
                ('need', models.ForeignKey(to='scheduler.Need')),
                ('registrationprofile', models.ForeignKey(
                    to='registration_history.OldRegistrationProfile')),
            ],
            options={
                'db_table': 'registration_registrationprofile_needs',
                'managed': False,
            },
        ),
        migrations.AddField(
            model_name='oldregistrationprofile',
            name='needs',
            field=models.ManyToManyField(to='scheduler.Need',
                                         verbose_name=b'registrierte Schichten',
                                         through='registration_history.OldRegistrationProfileNeed'),
        ),
        migrations.AddField(
            model_name='oldregistrationprofile',
            name='user',
            field=models.OneToOneField(verbose_name='user',
                                       to=settings.AUTH_USER_MODEL),
        ),
    ]

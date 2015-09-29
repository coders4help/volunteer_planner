# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings

from django.db import models, migrations


class Migration(migrations.Migration):
    replaces = [
        (b'registration_history', '0001_initial'),
        (b'registration_history', '0002_move_user_needs'),
        (b'registration_history', '0003_switch_to_managed_mode'),
        (b'registration_history', '0004_migrate_to_redux'),
        (b'registration_history', '0005_update_activated'),
        (b'registration_history', '0006_remove_model'),
        (b'registration', '0001_initial'),
        (b'registration', '0002_auto_20150819_0134'),
        (b'registration', '0003_auto_20150819_0140'),
        (b'registration', '0004_auto_20150903_2258'),
        (b'registration', '0004_auto_20150830_1945'),
        (b'registration', '0004_auto_20150822_1800'),
        (b'registration', '0005_merge'),
        (b'registration', '0006_remove_registrationprofile_interests')
    ]

    dependencies = [
        ('accounts', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('scheduler', '0021_add_shift_users'),
    ]

    operations = [
        migrations.CreateModel(
            name='RegistrationProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False,
                                        auto_created=True, primary_key=True)),
                ('activation_key', models.CharField(max_length=40,
                                                    verbose_name='activation key')),
                ('activated', models.BooleanField(default=False)),
                ('user', models.OneToOneField(verbose_name='user',
                                              to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'registration_registrationprofile',
                'managed': True,
                'verbose_name': 'registration profile',
                'verbose_name_plural': 'registration profiles',
            },
        ),
        migrations.AlterModelOptions(
            name='RegistrationProfile',
            options={'managed': False},
        ),
        migrations.RemoveField(
            model_name='RegistrationProfile',
            name='user',
        ),
        migrations.DeleteModel(
            name='RegistrationProfile',
        ),
    ]

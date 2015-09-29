# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):
    replaces = [(b'registration', '0001_initial'),
                (b'registration', '0002_auto_20150819_0134'),
                (b'registration', '0003_auto_20150819_0140'),
                (b'registration', '0004_auto_20150903_2258'),
                (b'registration', '0004_auto_20150830_1945'),
                (b'registration', '0004_auto_20150822_1800'),
                (b'registration', '0005_merge'),
                (b'registration', '0006_remove_registrationprofile_interests')]

    dependencies = [
        ('scheduler', '0007_auto_20150819_0138'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('scheduler', '0006_auto_20150819_0134'),
    ]

    operations = [
        migrations.CreateModel(
            name='RegistrationProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False,
                                        auto_created=True, primary_key=True)),
                ('activation_key', models.CharField(max_length=40,
                                                    verbose_name='activation key')),
                ('user', models.ForeignKey(verbose_name='user',
                                           to=settings.AUTH_USER_MODEL,
                                           unique=True)),
            ],
            options={
                'verbose_name': 'registration profile',
                'verbose_name_plural': 'registration profiles',
            },
        ),
        migrations.AlterModelOptions(
            name='registrationprofile',
            options={'verbose_name': 'Freiwillige',
                     'verbose_name_plural': 'Freiwillige'},
        ),
        migrations.AddField(
            model_name='registrationprofile',
            name='needs',
            field=models.ManyToManyField(to=b'scheduler.Need',
                                         verbose_name=b'registrierte Schichten'),
        ),
        migrations.AlterField(
            model_name='registrationprofile',
            name='user',
            field=models.OneToOneField(verbose_name='user',
                                       to=settings.AUTH_USER_MODEL),
        ),
    ]

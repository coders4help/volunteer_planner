# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scheduler', '0006_auto_20150819_0134'),
        ('registration', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='registrationprofile',
            options={'verbose_name': 'Freiwillige', 'verbose_name_plural': 'Freiwillige'},
        ),
        migrations.AddField(
            model_name='registrationprofile',
            name='interests',
            field=models.ForeignKey(default=1, to='scheduler.Topics'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='registrationprofile',
            name='needs',
            field=models.ManyToManyField(to='scheduler.Need'),
        ),
    ]

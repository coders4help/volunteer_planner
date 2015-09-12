# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scheduler', '0014_remove_need_activate'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='need',
            options={'verbose_name': 'shift', 'verbose_name_plural': 'shifts'},
        ),
        migrations.AlterField(
            model_name='need',
            name='location',
            field=models.ForeignKey(verbose_name='location', to='scheduler.Location'),
        ),
        migrations.AlterField(
            model_name='need',
            name='slots',
            field=models.IntegerField(verbose_name='num_volunteers', blank=True),
        ),
        migrations.AlterField(
            model_name='need',
            name='time_period_from',
            field=models.ForeignKey(related_name='time_from', verbose_name='time_from', to='scheduler.TimePeriods'),
        ),
        migrations.AlterField(
            model_name='need',
            name='topic',
            field=models.ForeignKey(verbose_name='helptype', to='scheduler.Topics', help_text='helptype_text'),
        ),
    ]

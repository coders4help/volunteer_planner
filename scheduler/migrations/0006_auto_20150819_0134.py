# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scheduler', '0005_need_location'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='location',
            options={'verbose_name': 'Ort', 'verbose_name_plural': 'Orte'},
        ),
        migrations.AlterModelOptions(
            name='need',
            options={'verbose_name': 'Schicht', 'verbose_name_plural': 'Schichten'},
        ),
        migrations.AlterModelOptions(
            name='timeperiods',
            options={'verbose_name': 'Zeitspanne', 'verbose_name_plural': 'Zeitspannen'},
        ),
        migrations.AlterModelOptions(
            name='topics',
            options={'verbose_name': 'Hilfebereich', 'verbose_name_plural': 'Hilfebereiche'},
        ),
        migrations.AlterModelOptions(
            name='volunteers',
            options={'verbose_name': 'Freiwillige', 'verbose_name_plural': 'Freiwillige'},
        ),
        migrations.AlterField(
            model_name='need',
            name='location',
            field=models.ForeignKey(verbose_name=b'Ort', to='scheduler.Location', on_delete=models.CASCADE),
        ),
        migrations.AlterField(
            model_name='need',
            name='time_period_from',
            field=models.ForeignKey(related_name='time_from', verbose_name=b'Anfangszeit', to='scheduler.TimePeriods', on_delete=models.CASCADE),
        ),
        migrations.AlterField(
            model_name='need',
            name='topic',
            field=models.ForeignKey(verbose_name=b'Hilfetyp', to='scheduler.Topics',
                                    help_text='Jeder Hilfetyp hat so viele Planelemente wie es Arbeitsschichten geben '
                                              'soll. Dies ist EINE Arbeitsschicht f\xfcr einen bestimmten Tag',
                                    on_delete=models.CASCADE),
        ),
    ]

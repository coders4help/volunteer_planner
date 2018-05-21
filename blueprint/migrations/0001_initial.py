# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scheduler', '0009_auto_20150823_1546'),
    ]

    operations = [
        migrations.CreateModel(
            name='BluePrintCreator',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255, verbose_name=b'Name der Vorlage')),
                ('location', models.ForeignKey(verbose_name=b'Ort', to='scheduler.Location', on_delete=models.CASCADE)),
            ],
            options={
                'verbose_name': 'Vorlage',
                'verbose_name_plural': 'Vorlagen',
            },
        ),
        migrations.CreateModel(
            name='NeedBluePrint',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('from_time', models.CharField(max_length=5, verbose_name=b'Uhrzeit von')),
                ('to_time', models.CharField(max_length=5, verbose_name=b'Uhrzeit bis')),
                ('topic', models.ForeignKey(verbose_name=b'Hilfetyp', to='scheduler.Topics', on_delete=models.CASCADE)),
            ],
            options={
                'verbose_name': 'Schicht Vorlage',
                'verbose_name_plural': 'Schicht Vorlagen',
            },
        ),
        migrations.AddField(
            model_name='blueprintcreator',
            name='needs',
            field=models.ManyToManyField(to='blueprint.NeedBluePrint', verbose_name=b'Schichten'),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Need',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('slots', models.IntegerField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='TimePeriods',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_time', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Topics',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField(max_length=20000, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Volunteers',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('interests', models.ForeignKey(to='scheduler.Topics')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='need',
            name='time_period_from',
            field=models.ForeignKey(related_name='time_from', to='scheduler.TimePeriods'),
        ),
        migrations.AddField(
            model_name='need',
            name='time_period_to',
            field=models.ForeignKey(related_name='time_to', to='scheduler.TimePeriods'),
        ),
        migrations.AddField(
            model_name='need',
            name='topic',
            field=models.ForeignKey(to='scheduler.Topics'),
        ),
    ]

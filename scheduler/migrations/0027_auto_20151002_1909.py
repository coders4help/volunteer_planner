# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
        ('places', '0003_auto_20151002_1909'),
        ('scheduler', '0026_auto_20151002_0150'),
    ]

    operations = [
        migrations.CreateModel(
            name='Enrolment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('joined_shift_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Enrolment for shift',
                'verbose_name_plural': 'Enrolments for shifts',
            },
        ),
        migrations.CreateModel(
            name='RecurringEvent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True)),
                ('weekday', models.IntegerField(choices=[(0, 'Monday'), (1, 'Tuesday'), (2, 'Wednesday'), (3, 'Thursday'), (4, 'Friday'), (5, 'Saturday'), (6, 'Sunday')])),
                ('needed_volunteers', models.IntegerField(verbose_name='number of needed volunteers')),
                ('start_time', models.TimeField(verbose_name='Starting time')),
                ('end_time', models.TimeField(verbose_name='Ending time')),
                ('first_date', models.DateTimeField(verbose_name='First occurrence')),
                ('last_date', models.DateTimeField(verbose_name='Last occurrence')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at')),
                ('disabled', models.BooleanField(default=False, verbose_name='Disabled')),
            ],
        ),
        migrations.CreateModel(
            name='Shift',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('needed_volunteers', models.IntegerField(verbose_name='number of needed volunteers')),
                ('start_time', models.DateTimeField(verbose_name='starting time', db_index=True)),
                ('end_time', models.DateTimeField(verbose_name='ending time', db_index=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at')),
                ('published_at', models.DateTimeField(null=True, verbose_name='published at')),
                ('cancelled_at', models.DateTimeField(null=True, verbose_name='cancelled at')),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True)),
            ],
        ),
        migrations.AddField(
            model_name='shift',
            name='task',
            field=models.ForeignKey(verbose_name='', to='scheduler.Task', help_text=''),
        ),
        migrations.AddField(
            model_name='shift',
            name='volunteers',
            field=models.ManyToManyField(related_name='shifts', through='scheduler.Enrolment', to='accounts.UserAccount'),
        ),
        migrations.AddField(
            model_name='shift',
            name='workplace',
            field=models.ForeignKey(verbose_name='', to='places.Workplace', help_text=''),
        ),
        migrations.AddField(
            model_name='recurringevent',
            name='task',
            field=models.ForeignKey(to='scheduler.Task'),
        ),
        migrations.AddField(
            model_name='recurringevent',
            name='workplace',
            field=models.ForeignKey(to='places.Workplace'),
        ),
        migrations.AddField(
            model_name='enrolment',
            name='shift',
            field=models.ForeignKey(to='scheduler.Shift'),
        ),
        migrations.AddField(
            model_name='enrolment',
            name='user',
            field=models.ForeignKey(to='accounts.UserAccount'),
        ),
        migrations.AlterUniqueTogether(
            name='enrolment',
            unique_together=set([('user', 'shift')]),
        ),
    ]

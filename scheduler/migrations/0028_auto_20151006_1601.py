# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
        ('organizations', '0004_remits_and_tasks'),
        ('scheduler', '0027_auto_20151003_1941'),
    ]

    operations = [
        migrations.CreateModel(
            name='Enrolment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('joined_shift_at', models.DateTimeField(auto_now_add=True, verbose_name='joined at')),
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
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('description', models.TextField(verbose_name='description', blank=True)),
                ('weekday', models.IntegerField(verbose_name='weekday', choices=[(0, 'Monday'), (1, 'Tuesday'), (2, 'Wednesday'), (3, 'Thursday'), (4, 'Friday'), (5, 'Saturday'), (6, 'Sunday')])),
                ('needed_volunteers', models.IntegerField(verbose_name='number of needed volunteers')),
                ('start_time', models.TimeField(verbose_name='Starting time')),
                ('end_time', models.TimeField(verbose_name='Ending time')),
                ('first_date', models.DateTimeField(verbose_name='First occurrence')),
                ('last_date', models.DateTimeField(verbose_name='Last occurrence')),
                ('disabled', models.BooleanField(default=False, verbose_name='Disabled')),
                ('task', models.ForeignKey(verbose_name='task', to='organizations.Task')),
                ('workplace', models.ForeignKey(verbose_name='workplace', to='organizations.Workplace')),
            ],
        ),
        migrations.CreateModel(
            name='Shift',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('needed_volunteers', models.IntegerField(verbose_name='number of needed volunteers')),
                ('start_time', models.DateTimeField(verbose_name='starting time', db_index=True)),
                ('end_time', models.DateTimeField(verbose_name='ending time', db_index=True)),
                ('task', models.ForeignKey(verbose_name='task', to='organizations.Task', help_text='')),
                ('volunteers', models.ManyToManyField(related_name='shifts', verbose_name='volunteers', through='scheduler.Enrolment', to='accounts.UserAccount')),
                ('workplace', models.ForeignKey(verbose_name='workplace', to='organizations.Workplace', help_text='')),
            ],
        ),
        migrations.AddField(
            model_name='enrolment',
            name='shift',
            field=models.ForeignKey(related_name='enrolled_users', verbose_name='shift', to='scheduler.Shift'),
        ),
        migrations.AddField(
            model_name='enrolment',
            name='user_account',
            field=models.ForeignKey(related_name='enrolments', verbose_name='user account', to='accounts.UserAccount'),
        ),
        migrations.AlterUniqueTogether(
            name='enrolment',
            unique_together=set([('user_account', 'shift')]),
        ),
        migrations.AlterField(
            model_name='shift',
            name='task',
            field=models.ForeignKey(verbose_name='task', to='organizations.Task', help_text=''),
        ),
        migrations.AlterField(
            model_name='shift',
            name='workplace',
            field=models.ForeignKey(verbose_name='workplace', to='organizations.Workplace', help_text=''),
        ),
    ]

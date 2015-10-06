# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0002_migrate_locations_to_facilities'),
    ]

    operations = [
        migrations.CreateModel(
            name='Workplace',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=256, verbose_name='name')),
                ('slug', models.SlugField(verbose_name='slug')),
                ('description', models.TextField(verbose_name='description', blank=True)),
                ('facility', models.ForeignKey(related_name='workplaces', verbose_name='facility', to='organizations.Facility')),
            ],
            options={
                'ordering': ('facility', 'name'),
                'verbose_name': 'workplace',
                'verbose_name_plural': 'workplaces',
            },
        ),
    ]

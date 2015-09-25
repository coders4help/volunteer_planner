# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Area',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=50, verbose_name='name')),
                ('slug', models.SlugField(verbose_name='slug')),
            ],
            options={
                'ordering': ('region', 'name'),
                'verbose_name': 'area',
                'verbose_name_plural': 'areas',
            },
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=50, verbose_name='name')),
                ('slug', models.SlugField(verbose_name='slug')),
            ],
            options={
                'ordering': ('name',),
                'verbose_name': 'country',
                'verbose_name_plural': 'countries',
            },
        ),
        migrations.CreateModel(
            name='Place',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=50, verbose_name='name')),
                ('slug', models.SlugField(verbose_name='slug')),
                ('area', models.ForeignKey(related_name='places', verbose_name='place', to='places.Area')),
            ],
            options={
                'ordering': ('area', 'name'),
                'verbose_name': 'place',
                'verbose_name_plural': 'places',
            },
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=50, verbose_name='name')),
                ('slug', models.SlugField(verbose_name='slug')),
                ('country', models.ForeignKey(related_name='regions', verbose_name='country', to='places.Country')),
            ],
            options={
                'ordering': ('country', 'name'),
                'verbose_name': 'region',
                'verbose_name_plural': 'regions',
            },
        ),
        migrations.AddField(
            model_name='area',
            name='region',
            field=models.ForeignKey(related_name='areas', verbose_name='region', to='places.Region'),
        ),
    ]

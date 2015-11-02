# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import sys

from django.db import models, migrations
from django.utils.text import slugify
from common.migrations import skip


def add_slugs(apps, schema_editor):
    Organization = apps.get_model('organizations', 'Organization')
    Facility = apps.get_model('organizations', 'Facility')

    for model in (Organization, Facility):
        for instance in model.objects.all():
            instance.slug = slugify(instance.name)
            instance.save()
            sys.stdout.write(u'{} -> {}\n'.format(instance, instance.slug))


class Migration(migrations.Migration):
    dependencies = [
        ('organizations', '0007_auto_20151023_2129'),
    ]

    operations = [
        migrations.AddField(
            model_name='facility',
            name='slug',
            field=models.SlugField(null=True, verbose_name='slug', blank=True),
        ),
        migrations.AddField(
            model_name='organization',
            name='slug',
            field=models.SlugField(null=True, verbose_name='slug', blank=True),
        ),

        migrations.RunPython(add_slugs, skip),

        migrations.AlterField(
            model_name='facility',
            name='slug',
            field=models.SlugField(verbose_name='slug'),
        ),
        migrations.AlterField(
            model_name='organization',
            name='slug',
            field=models.SlugField(verbose_name='slug'),
        ),
    ]

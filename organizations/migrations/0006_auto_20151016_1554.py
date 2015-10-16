# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0005_auto_20151016_1520'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='news',
            options={'verbose_name': 'News', 'verbose_name_plural': 'News'},
        ),
        migrations.RemoveField(
            model_name='news',
            name='news',
        ),
        migrations.AddField(
            model_name='news',
            name='facility',
            field=models.ForeignKey(related_name='facility', to='organizations.Facility', null=True),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0002_auto_20150823_1658'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='subtitle',
            field=models.CharField(max_length=255, null=True, verbose_name='subtitle', blank=True),
        ),
        migrations.AlterField(
            model_name='notification',
            name='text',
            field=models.TextField(max_length=20055, verbose_name='articletext'),
        ),
        migrations.AlterField(
            model_name='notification',
            name='title',
            field=models.CharField(max_length=255, verbose_name='title'),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0006_auto_20151016_1554'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='date_created',
            field=models.DateTimeField(auto_now=True, verbose_name='date published'),
        ),
    ]

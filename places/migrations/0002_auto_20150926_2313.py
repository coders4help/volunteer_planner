# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('places', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='place',
            name='area',
            field=models.ForeignKey(related_name='places', verbose_name='area', to='places.Area', on_delete=models.CASCADE),
        ),
    ]

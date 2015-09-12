# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scheduler', '0014_remove_need_activate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='need',
            name='slots',
            field=models.IntegerField(verbose_name=b'Anz. benoetigter Freiwillige'),
        ),
    ]

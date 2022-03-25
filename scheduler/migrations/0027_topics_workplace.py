# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("scheduler", "0026_auto_20151002_0150"),
    ]

    operations = [
        migrations.AddField(
            model_name="topics",
            name="workplace",
            field=models.CharField(
                max_length=255, verbose_name="workplace", blank=True
            ),
        ),
    ]

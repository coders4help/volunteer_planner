# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("notifications", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="notification",
            name="subtitle",
            field=models.CharField(
                max_length=255, null=True, verbose_name=b"Untertitel", blank=True
            ),
        ),
    ]

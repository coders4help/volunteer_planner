# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ("scheduler", "0003_volunteers_needs"),
    ]

    operations = [
        migrations.CreateModel(
            name="Location",
            fields=[
                (
                    "id",
                    models.AutoField(
                        verbose_name="ID",
                        serialize=False,
                        auto_created=True,
                        primary_key=True,
                    ),
                ),
                ("name", models.CharField(max_length=255, blank=True)),
                ("street", models.CharField(max_length=255, blank=True)),
                ("city", models.CharField(max_length=255, blank=True)),
                ("postal_code", models.CharField(max_length=5, blank=True)),
                ("longitude", models.CharField(max_length=30, blank=True)),
                ("altitude", models.CharField(max_length=30, blank=True)),
                ("additional_info", models.TextField(max_length=300000, blank=True)),
            ],
        ),
        migrations.AlterField(
            model_name="need",
            name="slots",
            field=models.IntegerField(
                verbose_name=b"Anz. benoetigter Freiwillige", blank=True
            ),
        ),
    ]

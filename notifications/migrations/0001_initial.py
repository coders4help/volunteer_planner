# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("scheduler", "0009_auto_20150823_1546"),
    ]

    operations = [
        migrations.CreateModel(
            name="Notification",
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
                ("slug", models.SlugField(max_length=255, auto_created=True)),
                ("creation_date", models.DateField(auto_now=True)),
                ("title", models.CharField(max_length=255, verbose_name=b"Titel")),
                (
                    "subtitle",
                    models.CharField(max_length=255, verbose_name=b"Untertitel"),
                ),
                (
                    "text",
                    models.TextField(max_length=20055, verbose_name=b"Artikeltext"),
                ),
                (
                    "location",
                    models.ForeignKey(
                        to="scheduler.Location", on_delete=models.CASCADE
                    ),
                ),
            ],
        ),
    ]

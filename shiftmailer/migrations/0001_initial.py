# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ("scheduler", "0009_auto_20150823_1546"),
    ]

    operations = [
        migrations.CreateModel(
            name="Mailer",
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
                (
                    "first_name",
                    models.CharField(max_length=255, verbose_name=b"Vorname"),
                ),
                (
                    "last_name",
                    models.CharField(max_length=255, verbose_name=b"Nachname"),
                ),
                (
                    "position",
                    models.CharField(max_length=255, verbose_name=b"Position"),
                ),
                (
                    "organization",
                    models.CharField(max_length=255, verbose_name=b"Organisation"),
                ),
                ("email", models.EmailField(max_length=254, verbose_name=b"Email")),
                (
                    "location",
                    models.ForeignKey(
                        to="scheduler.Location", on_delete=models.CASCADE
                    ),
                ),
            ],
        ),
    ]

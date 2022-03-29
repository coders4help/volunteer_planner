# Generated by Django 4.0.3 on 2022-03-29 14:52

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0001_initial"),
        ("scheduler", "0040_min_shift_slots"),
    ]

    operations = [
        migrations.CreateModel(
            name="ShiftMessageToHelpers",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("message", models.TextField(verbose_name="Message")),
                (
                    "send_date",
                    models.DateTimeField(
                        default=datetime.datetime(2022, 3, 29, 14, 52, 42, 111075)
                    ),
                ),
                ("recipients", models.ManyToManyField(to="accounts.useraccount")),
                (
                    "sender",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="msg_sender",
                        to="accounts.useraccount",
                    ),
                ),
                (
                    "shift",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="scheduler.shift",
                    ),
                ),
            ],
        ),
    ]

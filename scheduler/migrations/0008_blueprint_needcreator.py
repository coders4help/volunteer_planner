from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("scheduler", "0007_auto_20150819_0138"),
    ]

    operations = [
        migrations.CreateModel(
            name="BluePrint",
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
                ("titel", models.CharField(max_length=255, blank=True)),
                ("day", models.DateField(verbose_name=b"Tag, der als Vorlage dient")),
                (
                    "location",
                    models.ForeignKey(
                        verbose_name=b"Ort",
                        to="scheduler.Location",
                        on_delete=models.CASCADE,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="NeedCreator",
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
                    "time_from",
                    models.CharField(
                        help_text=b"Format: 07:30",
                        max_length=5,
                        verbose_name=b"Uhrzeit Anfang",
                    ),
                ),
                (
                    "time_to",
                    models.CharField(
                        help_text=b"Format: 07:30",
                        max_length=5,
                        verbose_name=b"Uhrzeit Ende",
                    ),
                ),
                (
                    "slots",
                    models.IntegerField(
                        verbose_name=b"Anz. benoetigter Freiwillige", blank=True
                    ),
                ),
                ("apply_from", models.DateField(verbose_name=b"anwenden ab dem Tag")),
                ("apply_to", models.DateField(verbose_name=b"anwenden bis dem Tag")),
                (
                    "location",
                    models.ForeignKey(
                        verbose_name=b"Ort",
                        to="scheduler.Location",
                        on_delete=models.CASCADE,
                    ),
                ),
                (
                    "topic",
                    models.ForeignKey(
                        verbose_name=b"Hilfetyp",
                        to="scheduler.Topics",
                        on_delete=models.CASCADE,
                    ),
                ),
            ],
        ),
    ]

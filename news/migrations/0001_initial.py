from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("organizations", "0005_auto_20151021_1153"),
    ]

    operations = [
        migrations.CreateModel(
            name="News",
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
                (
                    "creation_date",
                    models.DateField(auto_now=True, verbose_name="creation date"),
                ),
                ("title", models.CharField(max_length=255, verbose_name="title")),
                (
                    "subtitle",
                    models.CharField(
                        max_length=255, null=True, verbose_name="subtitle", blank=True
                    ),
                ),
                (
                    "text",
                    models.TextField(max_length=20055, verbose_name="articletext"),
                ),
                (
                    "facility",
                    models.ForeignKey(
                        blank=True,
                        to="organizations.Facility",
                        null=True,
                        on_delete=models.SET_NULL,
                    ),
                ),
                (
                    "organization",
                    models.ForeignKey(
                        blank=True,
                        to="organizations.Organization",
                        null=True,
                        on_delete=models.SET_NULL,
                    ),
                ),
            ],
        ),
    ]

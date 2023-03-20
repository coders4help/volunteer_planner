from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("organizations", "0003_workplace"),
    ]

    operations = [
        migrations.CreateModel(
            name="Task",
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
                ("name", models.CharField(max_length=256, verbose_name="name")),
                (
                    "description",
                    models.TextField(verbose_name="description", blank=True),
                ),
                (
                    "facility",
                    models.ForeignKey(
                        related_name="tasks",
                        verbose_name="facility",
                        to="organizations.Facility",
                        on_delete=models.CASCADE,
                    ),
                ),
            ],
            options={
                "ordering": ("facility", "name"),
                "verbose_name": "task",
                "verbose_name_plural": "tasks",
            },
        ),
    ]

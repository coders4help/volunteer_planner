from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("organizations", "0004_add_tasks"),
    ]

    operations = [
        migrations.CreateModel(
            name="ScheduleTemplate",
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
                    "facility",
                    models.ForeignKey(
                        related_name="schedule_templates",
                        verbose_name="facility",
                        to="organizations.Facility",
                        on_delete=models.CASCADE,
                    ),
                ),
            ],
            options={
                "ordering": ("facility",),
                "verbose_name": "schedule template",
                "verbose_name_plural": "schedule templates",
            },
        ),
        migrations.CreateModel(
            name="ShiftTemplate",
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
                    "slots",
                    models.IntegerField(verbose_name="number of needed volunteers"),
                ),
                (
                    "starting_time",
                    models.TimeField(verbose_name="starting time", db_index=True),
                ),
                (
                    "ending_time",
                    models.TimeField(verbose_name="ending time", db_index=True),
                ),
                ("days", models.PositiveIntegerField(default=0, verbose_name="days")),
                (
                    "schedule_template",
                    models.ForeignKey(
                        related_name="shift_templates",
                        verbose_name="schedule template",
                        to="scheduletemplates.ScheduleTemplate",
                        on_delete=models.CASCADE,
                    ),
                ),
                (
                    "task",
                    models.ForeignKey(
                        related_name="+",
                        verbose_name="task",
                        to="organizations.Task",
                        on_delete=models.CASCADE,
                    ),
                ),
                (
                    "workplace",
                    models.ForeignKey(
                        related_name="+",
                        verbose_name="workplace",
                        blank=True,
                        to="organizations.Workplace",
                        null=True,
                        on_delete=models.SET_NULL,
                    ),
                ),
            ],
        ),
    ]

from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0001_initial"),
        ("scheduler", "0020_Fix_Working_Hours"),
    ]

    operations = [
        migrations.CreateModel(
            name="ShiftHelper",
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
                ("joined_shift_at", models.DateTimeField(auto_now_add=True)),
                (
                    "need",
                    models.ForeignKey(
                        related_name="shift_helpers",
                        to="scheduler.Need",
                        on_delete=models.CASCADE,
                    ),
                ),
                (
                    "user_account",
                    models.ForeignKey(
                        related_name="shift_helpers",
                        to="accounts.UserAccount",
                        on_delete=models.CASCADE,
                    ),
                ),
            ],
            options={
                "verbose_name": "shift helper",
                "verbose_name_plural": "shift helpers",
            },
        ),
        migrations.AddField(
            model_name="need",
            name="helpers",
            field=models.ManyToManyField(
                related_name="needs",
                through="scheduler.ShiftHelper",
                to="accounts.UserAccount",
            ),
        ),
    ]

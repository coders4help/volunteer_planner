from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("scheduler", "0019_remove_time_periods"),
    ]

    operations = [
        migrations.CreateModel(
            name="WorkDone",
            fields=[
                ("id", models.IntegerField(serialize=False, primary_key=True)),
                ("hours", models.IntegerField(verbose_name="working hours")),
            ],
            options={
                "db_table": "work_done",
                "managed": False,
            },
        ),
        migrations.AlterField(
            model_name="need",
            name="ending_time",
            field=models.DateTimeField(verbose_name="ending time", db_index=True),
        ),
        migrations.AlterField(
            model_name="need",
            name="starting_time",
            field=models.DateTimeField(verbose_name="starting time", db_index=True),
        ),
    ]

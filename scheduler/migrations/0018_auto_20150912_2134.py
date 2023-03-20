from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("scheduler", "0017_merge"),
    ]

    operations = [
        migrations.AlterField(
            model_name="need",
            name="slots",
            field=models.IntegerField(verbose_name="number of needed volunteers"),
        ),
        migrations.AlterField(
            model_name="need",
            name="time_period_from",
            field=models.ForeignKey(
                related_name="time_from",
                verbose_name="time from",
                to="scheduler.TimePeriods",
                on_delete=models.CASCADE,
            ),
        ),
    ]

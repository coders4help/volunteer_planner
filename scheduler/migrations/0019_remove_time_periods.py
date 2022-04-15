from __future__ import unicode_literals

from django.db import migrations, models


def skip(*_):
    pass


def _restore_time_periods(apps, schema_editor):
    shift_model = apps.get_model("scheduler", "Need")
    tp_model = apps.get_model("scheduler", "TimePeriods")
    for shift in shift_model.objects.select_related(
        "time_period_from", "time_period_to"
    ):

        from_tp = tp_model.objects.create(date_time=shift.starting_time)
        to_tp = tp_model.objects.create(date_time=shift.ending_time)

        shift.time_period_from = from_tp
        shift.time_period_to = to_tp

        shift.save()


def _set_starting_and_ending_times(apps, schema_editor):
    shift_model = apps.get_model("scheduler", "Need")
    for shift in shift_model.objects.select_related(
        "time_period_from", "time_period_to"
    ):

        shift.starting_time = shift.time_period_from.date_time
        shift.ending_time = shift.time_period_to.date_time

        shift.save()


class Migration(migrations.Migration):
    dependencies = [
        ("scheduler", "0018_auto_20150912_2134"),
    ]

    operations = [
        migrations.AddField(
            model_name="need",
            name="ending_time",
            field=models.DateTimeField(null=True, verbose_name="ending time"),
        ),
        migrations.AddField(
            model_name="need",
            name="starting_time",
            field=models.DateTimeField(null=True, verbose_name="starting time"),
        ),
        migrations.RunPython(_set_starting_and_ending_times, skip),
        migrations.AlterField(
            model_name="need",
            name="ending_time",
            field=models.DateTimeField(verbose_name="ending time"),
        ),
        migrations.AlterField(
            model_name="need",
            name="starting_time",
            field=models.DateTimeField(verbose_name="starting time"),
        ),
        migrations.AlterField(
            model_name="need",
            name="time_period_from",
            field=models.ForeignKey(
                related_name="time_from",
                verbose_name="time from",
                to="scheduler.TimePeriods",
                null=True,
                default=1,
                on_delete=models.SET_DEFAULT,
            ),
        ),
        migrations.AlterField(
            model_name="need",
            name="time_period_to",
            field=models.ForeignKey(
                related_name="time_to",
                to="scheduler.TimePeriods",
                null=True,
                default=1,
                on_delete=models.SET_DEFAULT,
            ),
        ),
        migrations.RunPython(skip, _restore_time_periods),
        migrations.RemoveField(
            model_name="need",
            name="time_period_from",
        ),
        migrations.RemoveField(
            model_name="need",
            name="time_period_to",
        ),
        migrations.DeleteModel(
            name="TimePeriods",
        ),
    ]

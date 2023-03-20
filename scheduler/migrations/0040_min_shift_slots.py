import django.core.validators
from django.db import migrations, models


def make_min_slots(apps, schema_editor):
    Shift = apps.get_model("schedule", "Shift")
    Shift.objects.filter(slots__lte=0).update(slots=1)


class Migration(migrations.Migration):
    dependencies = [
        ("scheduler", "0039_delete_workdone"),
    ]

    operations = [
        migrations.AlterField(
            model_name="shift",
            name="slots",
            field=models.PositiveIntegerField(
                help_text="number of needed volunteers",
                validators=[django.core.validators.MinValueValidator(1)],
                verbose_name="slots",
            ),
        ),
    ]

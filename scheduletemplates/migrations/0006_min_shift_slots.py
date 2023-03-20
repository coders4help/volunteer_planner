import django.core.validators
from django.db import migrations, models


def make_min_slots(apps, schema_editor):
    ShiftTemplate = apps.get_model("scheduletemplates", "ShiftTemplate")
    ShiftTemplate.objects.filter(slots__lte=0).update(slots=1)


class Migration(migrations.Migration):
    dependencies = [
        ("scheduletemplates", "0005_cascade_deletion"),
    ]

    operations = [
        migrations.RunPython(make_min_slots, migrations.RunPython.noop),
        migrations.AlterField(
            model_name="shifttemplate",
            name="slots",
            field=models.PositiveIntegerField(
                help_text="number of needed volunteers",
                validators=[django.core.validators.MinValueValidator(1)],
                verbose_name="slots",
            ),
        ),
    ]

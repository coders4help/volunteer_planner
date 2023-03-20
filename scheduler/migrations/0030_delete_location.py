from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("scheduler", "0029_remove_need_location"),
        ("shiftmailer", "0004_location_to_facility"),
    ]

    operations = [
        migrations.AlterField(
            model_name="need",
            name="facility",
            field=models.ForeignKey(
                verbose_name="facility",
                to="organizations.Facility",
                on_delete=models.CASCADE,
            ),
        ),
        migrations.RemoveField(
            model_name="location",
            name="place",
        ),
        migrations.DeleteModel(
            name="Location",
        ),
    ]

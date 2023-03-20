from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("organizations", "0002_migrate_locations_to_facilities"),
        ("notifications", "0003_auto_20150912_2049"),
    ]

    operations = [
        migrations.AlterField(
            model_name="notification",
            name="location",
            field=models.ForeignKey(
                verbose_name="facility",
                to="organizations.Facility",
                on_delete=models.CASCADE,
            ),
        ),
        migrations.RenameField(
            model_name="notification",
            old_name="location",
            new_name="facility",
        ),
        migrations.AlterField(
            model_name="notification",
            name="facility",
            field=models.ForeignKey(
                to="organizations.Facility", on_delete=models.CASCADE
            ),
        ),
    ]

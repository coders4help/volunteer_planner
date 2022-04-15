from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("organizations", "0002_migrate_locations_to_facilities"),
        ("blueprint", "0002_needblueprint_slots"),
    ]

    operations = [
        migrations.AlterField(
            model_name="blueprintcreator",
            name="location",
            field=models.ForeignKey(
                verbose_name="facility",
                to="organizations.Facility",
                on_delete=models.CASCADE,
            ),
        ),
        migrations.RenameField(
            model_name="blueprintcreator",
            old_name="location",
            new_name="facility",
        ),
        migrations.AlterField(
            model_name="blueprintcreator",
            name="needs",
            field=models.ManyToManyField(
                to="blueprint.NeedBluePrint", verbose_name="shifts"
            ),
        ),
    ]

from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("scheduletemplates", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="shifttemplate",
            options={
                "ordering": ("schedule_template",),
                "verbose_name": "shift template",
                "verbose_name_plural": "shift templates",
            },
        ),
    ]

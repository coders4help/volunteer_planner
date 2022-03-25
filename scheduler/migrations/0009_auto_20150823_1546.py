# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("scheduler", "0008_blueprint_needcreator"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="blueprint",
            name="location",
        ),
        migrations.AlterModelOptions(
            name="needcreator",
            options={
                "verbose_name": "Bulk Schichten ",
                "verbose_name_plural": "Bulk Schichten",
            },
        ),
        migrations.DeleteModel(
            name="BluePrint",
        ),
    ]

from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("blueprint", "0004_merge"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="blueprintcreator",
            name="facility",
        ),
        migrations.RemoveField(
            model_name="blueprintcreator",
            name="needs",
        ),
        migrations.RemoveField(
            model_name="needblueprint",
            name="topic",
        ),
        migrations.DeleteModel(
            name="BluePrintCreator",
        ),
        migrations.DeleteModel(
            name="NeedBluePrint",
        ),
    ]

from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("scheduler", "0010_auto_20150904_0014"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="needcreator",
            name="location",
        ),
        migrations.RemoveField(
            model_name="needcreator",
            name="topic",
        ),
        migrations.DeleteModel(
            name="NeedCreator",
        ),
    ]

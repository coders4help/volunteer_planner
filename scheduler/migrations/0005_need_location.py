from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("scheduler", "0004_auto_20150818_2355"),
    ]

    operations = [
        migrations.AddField(
            model_name="need",
            name="location",
            field=models.ForeignKey(
                default=1, to="scheduler.Location", on_delete=models.CASCADE
            ),
            preserve_default=False,
        ),
    ]

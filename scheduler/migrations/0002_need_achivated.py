from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("scheduler", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="need",
            name="achivated",
            field=models.BooleanField(default=False),
        ),
    ]

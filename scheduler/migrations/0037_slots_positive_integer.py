from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("scheduler", "0036_shift_members_only"),
    ]

    operations = [
        migrations.AlterField(
            model_name="shift",
            name="slots",
            field=models.PositiveIntegerField(
                verbose_name="number of needed volunteers"
            ),
        ),
    ]

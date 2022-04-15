from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("organizations", "0010_membership_join_mode"),
    ]

    operations = [
        migrations.AddField(
            model_name="facility",
            name="timeline_enabled",
            field=models.PositiveSmallIntegerField(
                default=1,
                verbose_name="timeline",
                choices=[(0, "disabled"), (1, "enabled (collapsed)"), (2, "enabled")],
            ),
        ),
    ]

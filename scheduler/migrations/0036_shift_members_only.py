from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("scheduler", "0035_delete_topics_model"),
    ]

    operations = [
        migrations.AddField(
            model_name="shift",
            name="members_only",
            field=models.BooleanField(
                default=False,
                help_text="allow only members to help",
                verbose_name="members only",
            ),
        ),
    ]

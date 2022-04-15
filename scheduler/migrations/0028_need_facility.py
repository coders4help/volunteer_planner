from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("organizations", "0001_initial"),
        ("scheduler", "0027_topics_workplace"),
    ]

    operations = [
        migrations.AddField(
            model_name="need",
            name="facility",
            field=models.ForeignKey(
                verbose_name="facility",
                to="organizations.Facility",
                null=True,
                on_delete=models.CASCADE,
            ),
        ),
    ]

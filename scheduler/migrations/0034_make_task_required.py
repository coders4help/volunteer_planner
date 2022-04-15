from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("scheduler", "0033_migrate_topics"),
    ]

    operations = [
        migrations.AlterField(
            model_name="shift",
            name="task",
            field=models.ForeignKey(
                verbose_name="task", to="organizations.Task", on_delete=models.CASCADE
            ),
        ),
    ]

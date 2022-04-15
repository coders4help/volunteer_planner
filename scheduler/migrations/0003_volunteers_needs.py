from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("scheduler", "0002_need_achivated"),
    ]

    operations = [
        migrations.AddField(
            model_name="volunteers",
            name="needs",
            field=models.ManyToManyField(to="scheduler.Need"),
        ),
    ]

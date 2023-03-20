from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("scheduler", "0018_auto_20150912_2134"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="topics",
            options={"verbose_name": "help type", "verbose_name_plural": "help types"},
        ),
        migrations.AlterField(
            model_name="need",
            name="topic",
            field=models.ForeignKey(
                verbose_name="help type",
                to="scheduler.Topics",
                help_text="HELP_TYPE_HELP",
                on_delete=models.CASCADE,
            ),
        ),
    ]

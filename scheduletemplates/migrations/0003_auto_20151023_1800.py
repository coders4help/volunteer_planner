from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("scheduletemplates", "0002_auto_20151013_2229"),
    ]

    operations = [
        migrations.AlterField(
            model_name="shifttemplate",
            name="task",
            field=models.ForeignKey(
                verbose_name="task", to="organizations.Task", on_delete=models.CASCADE
            ),
        ),
        migrations.AlterField(
            model_name="shifttemplate",
            name="workplace",
            field=models.ForeignKey(
                verbose_name="workplace",
                blank=True,
                to="organizations.Workplace",
                null=True,
                on_delete=models.SET_NULL,
            ),
        ),
    ]

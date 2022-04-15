from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("shiftmailer", "0002_auto_20150912_2049"),
    ]

    operations = [
        migrations.AlterField(
            model_name="mailer",
            name="first_name",
            field=models.CharField(max_length=255, verbose_name="first name"),
        ),
        migrations.AlterField(
            model_name="mailer",
            name="last_name",
            field=models.CharField(max_length=255, verbose_name="last name"),
        ),
    ]

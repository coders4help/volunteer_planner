# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("organizations", "0006_auto_20151022_1445"),
    ]

    operations = [
        migrations.AlterField(
            model_name="facility",
            name="contact_info",
            field=models.TextField(verbose_name="contact info"),
        ),
        migrations.AlterField(
            model_name="organization",
            name="contact_info",
            field=models.TextField(verbose_name="contact info"),
        ),
    ]

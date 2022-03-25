# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ("content", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="flatpagetranslation",
            name="language",
            field=models.CharField(
                max_length=20,
                verbose_name="language",
                choices=[
                    (b"en", "English"),
                    (b"de", "German"),
                    (b"el", "Greek"),
                    (b"hu", "Hungarian"),
                    (b"sv", "Swedish"),
                ],
            ),
        ),
    ]

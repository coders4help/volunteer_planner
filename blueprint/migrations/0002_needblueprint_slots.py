# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ("blueprint", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="needblueprint",
            name="slots",
            field=models.IntegerField(
                default=4, verbose_name=b"Anz. benoetigter Freiwillige"
            ),
            preserve_default=False,
        ),
    ]

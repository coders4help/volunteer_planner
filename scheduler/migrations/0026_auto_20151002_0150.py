# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("scheduler", "0025_merge"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="shifthelper",
            unique_together=set([("user_account", "need")]),
        ),
    ]

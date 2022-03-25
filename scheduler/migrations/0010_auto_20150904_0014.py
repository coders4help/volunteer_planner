# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("scheduler", "0009_auto_20150823_1546"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="location",
            options={"permissions": (("can_view", "User can view location"),)},
        ),
    ]

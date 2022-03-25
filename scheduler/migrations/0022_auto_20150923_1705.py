# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ("scheduler", "0021_merge"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="location",
            options={
                "ordering": ("name",),
                "verbose_name": "location",
                "verbose_name_plural": "locations",
                "permissions": (("can_view", "User can view location"),),
            },
        ),
    ]

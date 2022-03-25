# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ("scheduletemplates", "0003_auto_20151023_1800"),
    ]

    operations = [
        migrations.AddField(
            model_name="shifttemplate",
            name="members_only",
            field=models.BooleanField(
                default=False,
                help_text="allow only members to help",
                verbose_name="members only",
            ),
        ),
    ]

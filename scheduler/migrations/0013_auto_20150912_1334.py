# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scheduler', '0012_rename_location_model_field_altitude_to_latitude'),
    ]

    operations = [
        migrations.RenameField(
            model_name='need',
            old_name='achivated',
            new_name='activate',
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):
    replaces = [
        ("notifications", "0001_initial"),
        ("notifications", "0002_auto_20150823_1658"),
        ("notifications", "0003_auto_20150912_2049"),
        ("notifications", "0004_auto_20151003_2033"),
        ("notifications", "0005_remove_notification_model"),
    ]

    dependencies = [
        ("scheduler", "0009_auto_20150823_1546"),
        ("organizations", "0002_migrate_locations_to_facilities"),
    ]

    operations = []

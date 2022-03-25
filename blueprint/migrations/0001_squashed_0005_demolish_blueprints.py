# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):
    replaces = [
        ("blueprint", "0001_initial"),
        ("blueprint", "0002_needblueprint_slots"),
        ("blueprint", "0003_auto_20151006_1341"),
        ("blueprint", "0003_auto_20151003_2033"),
        ("blueprint", "0004_merge"),
        ("blueprint", "0005_demolish_blueprints"),
    ]

    dependencies = [
        ("scheduler", "0009_auto_20150823_1546"),
        ("organizations", "0002_migrate_locations_to_facilities"),
    ]

    operations = []

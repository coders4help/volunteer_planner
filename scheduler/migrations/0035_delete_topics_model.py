# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('scheduler', '0034_make_task_required'),
        ('blueprint', '0005_demolish_blueprints')
    ]

    operations = [
        migrations.RemoveField(
            model_name='shift',
            name='topic',
        ),
        migrations.DeleteModel(
            name='Topics',
        ),
    ]

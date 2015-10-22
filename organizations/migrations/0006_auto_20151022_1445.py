# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0005_auto_20151021_1153'),
    ]

    operations = [
        migrations.AlterField(
            model_name='facilitymembership',
            name='role',
            field=models.PositiveIntegerField(default=2, verbose_name='role', choices=[(0, 'admin'), (1, 'manager'), (2, 'member')]),
        ),
        migrations.AlterField(
            model_name='organizationmembership',
            name='role',
            field=models.PositiveIntegerField(default=2, verbose_name='role', choices=[(0, 'admin'), (1, 'manager'), (2, 'member')]),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0004_add_tasks'),
        ('scheduler', '0031_rename_need_to_shift'),
    ]

    operations = [
        migrations.AddField(
            model_name='shift',
            name='task',
            field=models.ForeignKey(verbose_name='task', to='organizations.Task', null=True),
        ),
        migrations.AddField(
            model_name='shift',
            name='workplace',
            field=models.ForeignKey(verbose_name='workplace', to='organizations.Workplace', null=True, blank=True),
        ),
    ]

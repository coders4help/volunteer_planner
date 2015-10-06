# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scheduler', '0028_auto_20151006_1601'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shift',
            name='task',
            field=models.ForeignKey(verbose_name='task', to='organizations.Task', help_text=''),
        ),
        migrations.AlterField(
            model_name='shift',
            name='workplace',
            field=models.ForeignKey(verbose_name='workplace', to='organizations.Workplace', help_text=''),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scheduler', '0026_auto_20151002_0150'),
        ('organizations', '0002_migrate_locations_to_facilities'),
        ('shiftmailer', '0004_auto_20151003_2033'),
        ('blueprint', '0003_auto_20151003_2033'),
        ('notifications', '0004_auto_20151003_2033'),
    ]

    operations = [
        migrations.AlterField(
            model_name='need',
            name='location',
            field=models.ForeignKey(verbose_name='facility', to='organizations.Facility'),
        ),
        migrations.RemoveField(
            model_name='location',
            name='place',
        ),
        migrations.RenameField(
            model_name='need',
            old_name='location',
            new_name='facility',
        ),
        migrations.DeleteModel(
            name='Location',
        ),
    ]

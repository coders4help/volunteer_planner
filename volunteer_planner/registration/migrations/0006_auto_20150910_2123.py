# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scheduler', '0012_auto_20150910_2123'),
        ('registration', '0005_merge'),
    ]

    operations = [
        migrations.AddField(
            model_name='registrationprofile',
            name='shifts',
            field=models.ManyToManyField(to='scheduler.Need', verbose_name=b'registrierte Schichten', through='scheduler.scheduledRegPro'),
        ),
        migrations.AlterField(
            model_name='registrationprofile',
            name='needs',
            field=models.ManyToManyField(related_name='the_reg_pro', to='scheduler.Need'),
        ),
    ]

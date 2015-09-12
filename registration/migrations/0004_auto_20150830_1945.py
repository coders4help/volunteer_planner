# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0003_auto_20150819_0140'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registrationprofile',
            name='needs',
            field=models.ManyToManyField(to='scheduler.Need', verbose_name=b'registrierte Schichten'),
        ),
        migrations.AlterField(
            model_name='registrationprofile',
            name='user',
            field=models.OneToOneField(verbose_name='user', to=settings.AUTH_USER_MODEL),
        ),
    ]

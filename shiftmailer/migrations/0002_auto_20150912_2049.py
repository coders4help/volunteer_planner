# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shiftmailer', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mailer',
            name='email',
            field=models.EmailField(max_length=254, verbose_name='email'),
        ),
        migrations.AlterField(
            model_name='mailer',
            name='first_name',
            field=models.CharField(max_length=255, verbose_name='given_name'),
        ),
        migrations.AlterField(
            model_name='mailer',
            name='last_name',
            field=models.CharField(max_length=255, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='mailer',
            name='organization',
            field=models.CharField(max_length=255, verbose_name='organisation'),
        ),
        migrations.AlterField(
            model_name='mailer',
            name='position',
            field=models.CharField(max_length=255, verbose_name='position'),
        ),
    ]

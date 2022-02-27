# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('flatpages', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FlatPageExtraStyle',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('css', models.TextField(verbose_name='additional CSS', blank=True)),
                ('flatpage', models.OneToOneField(related_name='extra_style', verbose_name='additional style', to='flatpages.FlatPage', on_delete=models.CASCADE)),
            ],
            options={
                'verbose_name': 'additional flat page style',
                'verbose_name_plural': 'additional flat page styles',
            },
        ),
        migrations.CreateModel(
            name='FlatPageTranslation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('language', models.CharField(max_length=20, verbose_name='language', choices=[(b'de', 'German'), (b'en', 'English'), (b'hu', 'Hungarian'), (b'sv', 'Swedish')])),
                ('title', models.CharField(max_length=200, verbose_name='title', blank=True)),
                ('content', models.TextField(verbose_name='content', blank=True)),
                ('flatpage', models.ForeignKey(related_name='translations', verbose_name='flat page', to='flatpages.FlatPage', on_delete=models.CASCADE)),
            ],
            options={
                'verbose_name': 'flat page translation',
                'verbose_name_plural': 'flat page translations',
            },
        ),
        migrations.AlterUniqueTogether(
            name='flatpagetranslation',
            unique_together=set([('flatpage', 'language')]),
        ),
    ]

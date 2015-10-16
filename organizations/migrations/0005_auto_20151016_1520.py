# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0004_add_tasks'),
    ]

    operations = [
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=256, verbose_name='title')),
                ('text', models.TextField(verbose_name='text', blank=True)),
                ('date_created', models.DateField(auto_now=True, verbose_name='date published')),
                ('news', models.ForeignKey(to='organizations.Facility', null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='facilitymembership',
            name='facility',
            field=models.ForeignKey(related_query_name=b'membership', related_name='memberships', verbose_name='facility', to='organizations.Facility'),
        ),
        migrations.AlterField(
            model_name='facilitymembership',
            name='role',
            field=models.PositiveIntegerField(default=2, verbose_name='role', choices=[(0, 'Admin'), (1, 'Manager'), (2, 'Mitglied')]),
        ),
        migrations.AlterField(
            model_name='organizationmembership',
            name='organization',
            field=models.ForeignKey(related_query_name=b'membership', related_name='memberships', verbose_name='organization', to='organizations.Organization'),
        ),
        migrations.AlterField(
            model_name='organizationmembership',
            name='role',
            field=models.PositiveIntegerField(default=2, verbose_name='role', choices=[(0, 'Admin'), (1, 'Manager'), (2, 'Mitglied')]),
        ),
    ]

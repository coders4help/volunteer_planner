# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0004_add_tasks'),
    ]

    operations = [
        migrations.AlterField(
            model_name='facilitymembership',
            name='facility',
            field=models.ForeignKey(related_query_name=b'membership', related_name='memberships', verbose_name='facility', to='organizations.Facility', on_delete=models.CASCADE),
        ),
        migrations.AlterField(
            model_name='facilitymembership',
            name='role',
            field=models.PositiveIntegerField(default=2, verbose_name='role', choices=[(0, 'Admin'), (1, 'Manager'), (2, 'Mitglied')]),
        ),
        migrations.AlterField(
            model_name='organizationmembership',
            name='organization',
            field=models.ForeignKey(related_query_name=b'membership', related_name='memberships', verbose_name='organization', to='organizations.Organization', on_delete=models.CASCADE),
        ),
        migrations.AlterField(
            model_name='organizationmembership',
            name='role',
            field=models.PositiveIntegerField(default=2, verbose_name='role', choices=[(0, 'Admin'), (1, 'Manager'), (2, 'Mitglied')]),
        ),
    ]

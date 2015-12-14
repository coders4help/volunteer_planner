# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

from common.migrations import skip
from organizations.models import Membership


def add_default_join_mode(apps, _):
    organizationMembershipModel = apps.get_model('organizations', 'OrganizationMembership')

    facilityMembershipModel = apps.get_model('organizations', 'FacilityMembership')

    organizationMembershipModel.objects.update(status=Membership.Status.APPROVED)
    facilityMembershipModel.objects.update(status=Membership.Status.APPROVED)


class Migration(migrations.Migration):
    dependencies = [
        ('organizations', '0009_membership_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='facility',
            name='join_mode',
            field=models.PositiveSmallIntegerField(
                default=0,
                help_text='Who can join this facility?',
                verbose_name='join mode',
                choices=[
                    (0, 'by invitation'),
                    (1, 'anyone (approved by manager)'),
                    (2, 'anyone')
                ]
            ),
        ),
        migrations.AddField(
            model_name='organization',
            name='join_mode',
            field=models.PositiveSmallIntegerField(
                default=0,
                help_text='Who can join this organization?',
                verbose_name='join mode',
                choices=[
                    (0, 'by invitation'),
                    (1, 'anyone (approved by manager)'),
                    (2, 'anyone')
                ]
            ),
        ),
        migrations.RunPython(add_default_join_mode, skip)
    ]

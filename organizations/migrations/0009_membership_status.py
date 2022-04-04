# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models

from common.migrations import skip

# imported for status choices only, model is not used
from organizations.models import Membership


def approve_all(apps, _):
    organization_membership_model = apps.get_model(
        "organizations", "OrganizationMembership"
    )
    facility_membership_model = apps.get_model("organizations", "FacilityMembership")

    organization_membership_model.objects.update(status=Membership.Status.APPROVED)
    facility_membership_model.objects.update(status=Membership.Status.APPROVED)


class Migration(migrations.Migration):
    dependencies = [
        ("organizations", "0008_add_slug_field"),
    ]

    operations = [
        migrations.AddField(
            model_name="facilitymembership",
            name="status",
            field=models.PositiveSmallIntegerField(
                default=2,
                verbose_name="status",
                choices=[(0, "rejected"), (1, "pending"), (2, "approved")],
            ),
        ),
        migrations.AddField(
            model_name="organizationmembership",
            name="status",
            field=models.PositiveSmallIntegerField(
                default=2,
                verbose_name="status",
                choices=[(0, "rejected"), (1, "pending"), (2, "approved")],
            ),
        ),
        migrations.AlterField(
            model_name="facilitymembership",
            name="role",
            field=models.PositiveSmallIntegerField(
                default=2,
                verbose_name="role",
                choices=[(0, "admin"), (1, "manager"), (2, "member")],
            ),
        ),
        migrations.AlterField(
            model_name="organizationmembership",
            name="role",
            field=models.PositiveSmallIntegerField(
                default=2,
                verbose_name="role",
                choices=[(0, "admin"), (1, "manager"), (2, "member")],
            ),
        ),
        migrations.RunPython(approve_all, skip),
    ]

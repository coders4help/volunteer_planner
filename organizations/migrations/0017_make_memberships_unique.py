import logging

from django.db import migrations
from django.db.models import Count, Min

logger = logging.getLogger(__name__)


def check_is_staff(apps, user_account):
    OrganizationMembership = apps.get_model("organizations", "OrganizationMembership")
    FacilityMembership = apps.get_model("organizations", "FacilityMembership")

    logger.info("Checking is_staff for %s", user_account.user.username)

    if (
        not FacilityMembership.objects.filter(
            user_account=user_account, role__lt=2
        ).exists()
        and not OrganizationMembership.objects.filter(
            user_account=user_account, role__lt=2
        ).exists()
    ):
        logger.info("Revoking is_staff flag for user %s", user_account.user.username)
        user_account.user.is_staff = False
        user_account.user.save()


def squash_duplicate_organization_memberships(apps, schema_editor):
    OrganizationMembership = apps.get_model("organizations", "OrganizationMembership")

    members_with_duplicates = (
        OrganizationMembership.objects.order_by("user_account", "organization")
        .values("user_account", "organization")
        .annotate(number_of_roles=Count("role"), highest_role=Min("role"))
        .filter(number_of_roles__gt=1)
    )

    logger.info(
        "Found %s duplicate organization memberships", members_with_duplicates.count()
    )

    for member in members_with_duplicates:
        user_account = member["user_account"]
        organization = member["organization"]
        highest_role = member["highest_role"]

        user_memberships = OrganizationMembership.objects.filter(
            user_account=user_account,
            organization=organization,
        ).order_by("-status", "role")

        membership_to_keep = user_memberships.first()

        logger.info(
            "%s: keeping %s as (status=%s, role=%s) at %s",
            membership_to_keep.id,
            membership_to_keep.user_account.user.username,
            membership_to_keep.status,
            membership_to_keep.role,
            membership_to_keep.organization.name,
        )
        user_memberships.exclude(pk=membership_to_keep.pk).delete()

        if highest_role > 1:
            check_is_staff(apps, membership_to_keep.user_account)


def squash_duplicate_facility_memberships(apps, schema_editor):
    FacilityMembership = apps.get_model("organizations", "FacilityMembership")

    members_with_duplicates = (
        FacilityMembership.objects.order_by("user_account", "facility")
        .values("user_account", "facility")
        .annotate(number_of_roles=Count("role"), highest_role=Min("role"))
        .filter(number_of_roles__gt=1)
    )

    logger.info(
        "Found %s duplicate facility memberships", members_with_duplicates.count()
    )

    for member in members_with_duplicates:
        user_account = member["user_account"]
        facility = member["facility"]
        highest_role = member["highest_role"]

        user_memberships = FacilityMembership.objects.filter(
            user_account=user_account,
            facility=facility,
        ).order_by("-status", "role")

        membership_to_keep = user_memberships.first()

        logger.info(
            "%s: keeping %s as (status=%s, role=%s) at %s",
            membership_to_keep.id,
            membership_to_keep.user_account.user.username,
            membership_to_keep.status,
            membership_to_keep.role,
            membership_to_keep.facility.name,
        )
        user_memberships.exclude(pk=membership_to_keep.pk).delete()

        if highest_role > 1:
            check_is_staff(apps, membership_to_keep.user_account)


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0001_initial"),
        ("organizations", "0016_add_priority_help_text"),
    ]

    operations = [
        migrations.RunPython(
            squash_duplicate_organization_memberships, migrations.RunPython.noop
        ),
        migrations.RunPython(
            squash_duplicate_facility_memberships, migrations.RunPython.noop
        ),
        migrations.AlterUniqueTogether(
            name="facilitymembership",
            unique_together={("facility", "user_account")},
        ),
        migrations.AlterUniqueTogether(
            name="organizationmembership",
            unique_together={("organization", "user_account")},
        ),
    ]

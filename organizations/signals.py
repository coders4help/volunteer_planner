from django.contrib.auth.models import Group
from django.db import transaction
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import Membership, FacilityMembership, OrganizationMembership
from .settings import ORGANIZATION_MANAGER_GROUPNAME, FACILITY_MANAGER_GROUPNAME

class MembershipGroupUpdateException(Exception):
    pass


@transaction.atomic
def update_group_for_user(user_account, membership_set, group_name):
    """
    Check django.contrib.auth groups of user in user_account and add or remove groups for its memberships.

    :param user_account: the user account of the associated user to update the groups of
    :param membership_set: the membership set (reverse relation) to consider
    :param group_name: Name of group to be added or removed from the associated user
    :return:
    """
    user = user_account.user
    group = Group.objects.get(name=group_name)

    if membership_set.filter(role__lt=Membership.Roles.MEMBER).exists():
        user.groups.add(group)

        if not user.is_staff:
            user.is_staff = True
            user.save()
    else:
        user.groups.remove(group)
        # Revoking the user is_staff flag here is not save, because it can not be known, if the user has this flag
        # for another reason, too.


@receiver([post_save, post_delete], sender=FacilityMembership)
def handle_facility_membership_change(sender, instance, **kwargs):
    """
    Update the django.contrib.auth groups of the associated user object, whenever a facility membership for it is
    created, changed or deleted.
    """
    try:
        user_account = instance.user_account
        update_group_for_user(user_account, user_account.facilitymembership_set, FACILITY_MANAGER_GROUPNAME)

    except Exception as e:
        raise MembershipGroupUpdateException(f'facility -> "{FACILITY_MANAGER_GROUPNAME}"') from e


@receiver((post_save, post_delete), sender=OrganizationMembership)
def handle_organization_membership_change(sender, instance, **kwargs):
    """
    Update the django.contrib.auth groups of the associated user object, whenever a organization membership for it is
    created, changed or deleted.
    """
    try:
        user_account = instance.user_account
        update_group_for_user(user_account, user_account.organizationmembership_set, ORGANIZATION_MANAGER_GROUPNAME)

    except Exception as e:
        raise MembershipGroupUpdateException(f'organization -> "{FACILITY_MANAGER_GROUPNAME}"') from e

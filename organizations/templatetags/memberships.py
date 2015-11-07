# coding: utf-8

from django import template

from organizations.admin import get_cached_memberships
from organizations.models import Membership, FacilityMembership

register = template.Library()


@register.filter
def is_facility_member(user, facility, role=None):
    user_orgs, user_facilities = get_cached_memberships(
        user=user,
        roles=(Membership.Roles.ADMIN,
               Membership.Roles.MANAGER,
               Membership.Roles.MEMBER)
    )
    return facility.id in user_facilities or facility.organization.id in user_orgs


@register.filter
def is_membership_pending(user, facility):
    return FacilityMembership.objects.filter(facility=facility, user_account__user_id=user.id, status=Membership.Status.PENDING).exists()


@register.filter
def is_membership_rejected(user, facility):
    return FacilityMembership.objects.filter(facility=facility, user_account__user_id=user.id, status=Membership.Status.REJECTED).exists()


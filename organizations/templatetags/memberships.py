# coding: utf-8

from django import template
from django.db.models import Count

from organizations.admin import get_cached_memberships, filter_queryset_by_membership
from organizations.models import Membership, FacilityMembership

register = template.Library()


@register.filter
def is_facility_member(user, facility, role=None):
    user_orgs, user_facilities = get_cached_memberships(
        user=user,
        roles=(
            Membership.Roles.ADMIN,
            Membership.Roles.MANAGER,
            Membership.Roles.MEMBER,
        ),
    )
    return facility.id in user_facilities or facility.organization.id in user_orgs


@register.filter
def is_membership_pending(user, facility):
    return FacilityMembership.objects.filter(
        facility=facility,
        user_account__user_id=user.id,
        status=Membership.Status.PENDING,
    ).exists()


@register.filter
def is_membership_rejected(user, facility):
    return FacilityMembership.objects.filter(
        facility=facility,
        user_account__user_id=user.id,
        status=Membership.Status.REJECTED,
    ).exists()


@register.filter
def get_pending_membership_approvals(user):
    memberships = FacilityMembership.objects.filter(
        status=FacilityMembership.Status.PENDING
    ).order_by("facility")

    counters = (
        filter_queryset_by_membership(memberships, user)
        .values("facility")
        .annotate(count=Count("facility"))
    )

    result = dict(facilities=dict(), total=0)
    for counter in counters:
        result["facilities"][counter["facility"]] = counter["count"]
        result["total"] += counter["count"]

    return result

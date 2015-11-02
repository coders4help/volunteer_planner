# coding: utf-8

from django import template

from organizations.admin import get_cached_memberships
from organizations.models import Membership

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

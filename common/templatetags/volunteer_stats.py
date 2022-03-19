# coding: utf-8

from datetime import timedelta

from django import template
from django.contrib.auth.models import User
from django.db.models import Count
from django.utils import timezone

from organizations.models import Facility
from scheduler.models import Shift

register = template.Library()


@register.simple_tag
def get_facility_count():
    """
    Returns the number of total volunteer hours worked.
    """
    return Facility.objects.with_open_shifts().count()


@register.simple_tag
def get_volunteer_number():
    """
    Returns the number of active volunteer accounts (accounts are active).
    """
    return User.objects.filter(is_active=True).count()


@register.simple_tag
def get_volunteer_deleted_number():
    """
    Returns the number of deleted volunteer accounts (accounts are inactive and anonymized)
    """
    return User.objects.filter(is_active=False).count()


@register.simple_tag
def get_volunteer_hours():
    """
    Returns the number of total volunteer hours worked.
    """
    finished_shifts = Shift.objects.filter(starting_time__lte=timezone.now()).annotate(slots_done=Count("helpers"))
    delta = timedelta()
    for shift in finished_shifts:
        delta += shift.slots_done * (shift.ending_time - shift.starting_time)
    hours = int(delta.total_seconds() / 3600)
    return hours


@register.simple_tag
def get_volunteer_stats():
    """
    Returns all statistics concerning users, facilities and their shifts.
    """
    return {
        "volunteer_count": get_volunteer_number(),
        "volunteer_deleted_count": get_volunteer_deleted_number(),
        "facility_count": get_facility_count(),
        "volunteer_hours": get_volunteer_hours(),
    }

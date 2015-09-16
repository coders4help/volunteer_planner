import datetime
from django import template

from registration.models import RegistrationProfile

register = template.Library()


@register.simple_tag
def get_volunteer_hours():
    shifts = RegistrationProfile.objects.all() \
        .filter(needs__starting_time__lte=datetime.datetime.now())
    seconds = 0.0
    for shift in shifts:
        theshift = shift.needs.all()
        for single_shift in theshift:
            deelta = single_shift.ending_time - single_shift.starting_time
            seconds += deelta.total_seconds()
    return int(((seconds / 60) / 60))

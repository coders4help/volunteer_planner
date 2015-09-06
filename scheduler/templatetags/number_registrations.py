import datetime
from django import template

from registration.models import RegistrationProfile

register = template.Library()

@register.simple_tag
def get_volunteer_number():
    volunteers = RegistrationProfile.objects.all().count()
    return volunteers
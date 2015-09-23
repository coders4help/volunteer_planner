import datetime
from django import template
from django.contrib.auth.models import User

from registration.models import RegistrationProfile

register = template.Library()


@register.simple_tag
def get_volunteer_number():
    volunteers = User.objects.filter(is_active=True).count()
    return volunteers

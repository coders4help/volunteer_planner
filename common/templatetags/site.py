# coding: utf-8

# coding: utf-8
from django import conf, template

from django.contrib.sites.shortcuts import get_current_site

register = template.Library()


@register.simple_tag
def request_site(request):
    return get_current_site(request_site)


@register.simple_tag
def get_version():
    return conf.settings.VERSION

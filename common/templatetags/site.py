# coding: utf-8

# coding: utf-8

from django import template

from django.contrib.sites.shortcuts import get_current_site

register = template.Library()


@register.simple_tag
def request_site(request):
    return get_current_site(request_site)

# coding: utf-8

from django.contrib.sites.shortcuts import get_current_site
from django.utils.functional import SimpleLazyObject


def current_site(request):
    return {'site': SimpleLazyObject(lambda: get_current_site(request))}

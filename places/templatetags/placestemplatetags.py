# coding: utf-8

from django import template
from django.db.models import Count

from places.models import Place

register = template.Library()


@register.assignment_tag
def get_places_having_facilities():
    places = Place.objects.annotate(
        locations_count=Count('locations')).exclude(locations_count=0)

    return places

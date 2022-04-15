from django import template
from django.db.models import Count

from places.models import Place

register = template.Library()


@register.simple_tag
def get_places_having_facilities():
    places = (
        Place.objects.annotate(facility_count=Count("facilities"))
        .exclude(facility_count=0)
        .order_by("area__region__country", "area__region", "area")
    )

    return places

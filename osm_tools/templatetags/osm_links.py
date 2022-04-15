from django import template
from django.utils.translation import pgettext_lazy

register = template.Library()


def url_encoded_location(location):
    return "+".join("{}".format(location).split(" "))


@register.filter
def osm_search(location):
    location = url_encoded_location(location)
    pattern = pgettext_lazy(
        "maps search url pattern",
        "https://www.openstreetmap.org/search?query={location}",
    )
    return pattern.format(location=location)

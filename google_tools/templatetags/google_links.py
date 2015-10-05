# coding: utf-8

from django import template
from django.utils.translation import pgettext_lazy

register = template.Library()


def url_encoded_location(location):
    return u'+'.join(u'{}'.format(location).split(u' '))


@register.filter
def google_maps_search(location):
    location = url_encoded_location(location)
    pattern = pgettext_lazy('maps search url pattern',
                            u'https://www.google.com/maps/place/{location}')
    return pattern.format(location=location)


@register.filter
def google_maps_directions(destination, departure=None):
    departure = url_encoded_location(departure) if departure else ''
    destination = url_encoded_location(destination)

    pattern = pgettext_lazy(u'maps directions url pattern',
                            u'https://www.google.com/maps/dir/{departure}/{destination}/')

    return pattern.format(departure=departure, destination=destination)

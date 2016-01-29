# coding: utf-8

from django import template
from django.utils.translation import pgettext_lazy

register = template.Library()


def url_encoded_location(location):
    return u'+'.join(u'{}'.format(location).split(u' '))


@register.filter
def osm_search(location):
    location = url_encoded_location(location)
    pattern = pgettext_lazy('maps search url pattern',
                            u'https://www.openstreetmap.org/search?query={location}')
    return pattern.format(location=location)

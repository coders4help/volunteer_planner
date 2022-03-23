# coding: utf-8

from django.urls import re_path

from places.models import Country, Region, Area, Place

from .views import GeographicHelpdeskView

urlpatterns = [

    re_path(r'^(?P<slug>[-\w]+)/?$',
        GeographicHelpdeskView.as_view(model=Country),
        name='country-details'),

    re_path(r'^(?P<country__slug>[-\w]+)/(?P<slug>[-\w]+)/?$',
        GeographicHelpdeskView.as_view(model=Region),
        name='region-details'),

    re_path(
        r'^(?P<region__country__slug>[-\w]+)/(?P<region__slug>[-\w]+)/(?P<slug>[-\w]+)/?$',
        GeographicHelpdeskView.as_view(model=Area),
        name='area-details'),

    re_path(
        r'^(?P<area__region__country__slug>[-\w]+)/(?P<area__region__slug>[-\w]+)/(?P<area__slug>[-\w]+)/(?P<slug>[-\w]+)/?$',
        GeographicHelpdeskView.as_view(model=Place),
        name='place-details'),

]

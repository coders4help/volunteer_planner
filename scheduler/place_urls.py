# coding: utf-8

from django.conf.urls import url

from places.models import Country, Region, Area, Place

from .views import PlaceDetailView

urlpatterns = [

    url(r'^(?P<slug>[-\w]+)/?$',
        PlaceDetailView.as_view(model=Country),
        name='country-details'),

    url(r'^(?P<country__slug>[-\w]+)/(?P<slug>[-\w]+)/?$',
        PlaceDetailView.as_view(model=Region),
        name='region-details'),

    url(
        r'^(?P<region__country__slug>[-\w]+)/(?P<region__slug>[-\w]+)/(?P<slug>[-\w]+)/?$',
        PlaceDetailView.as_view(model=Area),
        name='area-details'),

    url(
        r'^(?P<area__region__country__slug>[-\w]+)/(?P<area__region__slug>[-\w]+)/(?P<area__slug>[-\w]+)/(?P<slug>[-\w]+)/?$',
        PlaceDetailView.as_view(model=Place),
        name='place-details'),

]

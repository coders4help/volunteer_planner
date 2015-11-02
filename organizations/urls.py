# coding: utf-8

from django.conf.urls import url

from .views import OrganizationView, FacilityView

urlpatterns = [

    url(r'^(?P<slug>[^/]+)/?$', OrganizationView.as_view(), name='organization'),
    url(r'^(?P<organization__slug>[^/]+)/(?P<slug>[^/]+)/?$', FacilityView.as_view(), name='facility'),

]

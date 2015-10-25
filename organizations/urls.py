# coding: utf-8

from django.conf.urls import url

from .views import OrganizationView, FacilityView

urlpatterns = [
    url(r'^(?P<pk>[^/]+)$', OrganizationView.as_view(), name='organization'),
    url(r'^(?P<orgpk>[^/]+)/facilities/(?P<pk>[^/]+)$', FacilityView.as_view(), name='facility')
]

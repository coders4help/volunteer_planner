# coding: utf-8

from django.conf.urls import url
from django.views.generic import TemplateView

from .views import (OrganizationView, FacilityView,
    ShiftManagementView, ShiftDeleteView)


urlpatterns = [
    url(r'^(?P<pk>[^/]+)$', OrganizationView.as_view(), name='organization'),
    url(r'^(?P<orgpk>[^/]+)/facilities/(?P<pk>[^/]+)$', FacilityView.as_view(), name='facility'),
    url(r'^delete/(?P<pk>\d+)/$', ShiftDeleteView.as_view(), name='shift_delete',),
    url(r'^', ShiftManagementView.as_view(), name="shift_management"),
]


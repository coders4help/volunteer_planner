# coding: utf-8

from django.conf.urls import url
from django.views.generic import TemplateView

from .views import (OrganizationView, FacilityView,
    ShiftManagementView, ShiftDeleteView)


urlpatterns = [
    url(r'^delete/(?P<pk>\d+)/$', ShiftDeleteView.as_view(),
        name='shift_delete',),
    url(r'^', ShiftManagementView.as_view(), name="shift_management"),
]


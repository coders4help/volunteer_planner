# coding: utf-8

from django.conf.urls import url
from django.views.generic import TemplateView

from .views import OrganizationView, FacilityView, ShiftManagementView


urlpatterns = [
    url(r'^', ShiftManagementView.as_view(), name="shift_management"),
]


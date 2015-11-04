# coding: utf-8

from django.conf.urls import url
from django.views.generic import TemplateView

from .views import OrganizationView, FacilityView, shift_management


urlpatterns = [
    url(r'^', shift_management, name="shift_management"),
]


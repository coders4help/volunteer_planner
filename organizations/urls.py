# coding: utf-8

from django.conf.urls import url
from django.views.generic.base import TemplateView

from .views import OrganizationView, FacilityView

urlpatterns = [
    url(r'^approvals/$', TemplateView.as_view(template_name="approvals.html"), name='approvals'),
    url(r'^(?P<slug>[^/]+)/?$', OrganizationView.as_view(), name='organization'),
    url(r'^(?P<organization__slug>[^/]+)/(?P<slug>[^/]+)/?$', FacilityView.as_view(), name='facility'),



]

# coding: utf-8

from django.conf.urls import url
from django.views.generic.base import TemplateView

from .views import OrganizationView, FacilityView, PendingApprovalsView

urlpatterns = [
    url(r'^approvals/$', PendingApprovalsView.as_view(), name='approvals'),
    url(r'^(?P<slug>[^/]+)/?$', OrganizationView.as_view(), name='organization'),
    url(r'^(?P<organization__slug>[^/]+)/(?P<slug>[^/]+)/?$', FacilityView.as_view(), name='facility'),



]

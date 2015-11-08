# coding: utf-8

from django.conf.urls import url
from django.views.generic.base import TemplateView

from .views import OrganizationView, FacilityView, PendingApprovalsView, managing_members_view

urlpatterns = [
    url(r'^manage_ajax/$',
        managing_members_view, name='manage-members-ajax'),
    url(r'^(?P<slug>[^/]+)/?$', OrganizationView.as_view(), name='organization'),

    url(r'^(?P<organization__slug>[^/]+)/(?P<slug>[^/]+)/?$', FacilityView.as_view(), name='facility'),

    url(r'^(?P<organization__slug>[^/]+)/(?P<slug>[^/]+)/manage/members/?$',
        PendingApprovalsView.as_view(), name='manage-members'),


]

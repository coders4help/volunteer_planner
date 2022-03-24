# coding: utf-8

from django.urls import re_path

from .views import OrganizationView, FacilityView, ManageFacilityMembersView, \
    managing_members_view

urlpatterns = [
    re_path(r'^(?P<slug>[^/]+)/?$', OrganizationView.as_view(),
        name='organization'),

    re_path(r'^(?P<organization__slug>[^/]+)/(?P<slug>[^/]+)/?$',
        FacilityView.as_view(), name='facility'),

    re_path(r'^(?P<organization__slug>[^/]+)/(?P<slug>[^/]+)/manage/members/?$',
        ManageFacilityMembersView.as_view(), name='manage-members'),

    re_path(
        r'^(?P<organization__slug>[^/]+)/(?P<slug>[^/]+)/manage/members/update/?$', managing_members_view, name='manage-members-ajax'),

]

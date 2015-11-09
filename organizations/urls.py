# coding: utf-8

from django.conf.urls import url

from .views import OrganizationView, FacilityView, ManageFacilityMembersView, \
    managing_members_view

urlpatterns = [
    url(r'^(?P<slug>[^/]+)/?$', OrganizationView.as_view(),
        name='organization'),

    url(r'^(?P<organization__slug>[^/]+)/(?P<slug>[^/]+)/?$',
        FacilityView.as_view(), name='facility'),

    url(r'^(?P<organization__slug>[^/]+)/(?P<slug>[^/]+)/manage/members/?$',
        ManageFacilityMembersView.as_view(), name='manage-members'),

    url(
        r'^(?P<organization__slug>[^/]+)/(?P<slug>[^/]+)/manage/members/update/?$', managing_members_view, name='manage-members-ajax'),

]

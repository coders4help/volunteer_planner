# coding: utf-8

from django.urls import re_path

from .views import HelpDesk, PlannerView, ShiftDetailView

urlpatterns = [
    re_path(r'^$', HelpDesk.as_view(), name="helpdesk"),

    # (A): needed for direct access of of a shift details site
    # via shifthelper.shift.get_absolute_url() (+"/direct/) (C) is needed for other things
    # (example of get_absolute_url() of a shift is: /helpdesk/facility190/shifts/2016/1/15/81 )
    re_path(r'^(?P<facility_slug>[^/]+)/shifts/(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/(?P<shift_id>\d+)/direct/?$',
        PlannerView.as_view(),
        name="planner_by_facility"),

    # (B):
    re_path(r'^(?P<facility_slug>[^/]+)/shifts/(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/?$',
        PlannerView.as_view(),
        name="planner_by_facility"),

    # (C):
    re_path(r'^(?P<facility_slug>[^/]+)/shifts/(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/(?P<shift_id>\d+)/?$',
        ShiftDetailView.as_view(),
        name="shift_details"),


]

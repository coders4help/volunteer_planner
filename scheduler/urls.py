# coding: utf-8

from django.conf.urls import url

from .views import HelpDesk, PlannerView, ShiftDetailView

urlpatterns = [
    url(r'^$', HelpDesk.as_view(), name="helpdesk"),

    # (A): needed for direct access of of a shift details site
    # via shifthelper.shift.get_absolute_url() (+"/direct/) (C) is needed for other things
    # (example of get_absolute_url() of a shift is: /helpdesk/facility190/shifts/2016/1/15/81 )
    url(r'^(?P<facility_slug>[^/]+)/shifts/(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/(?P<shift_id>\d+)/direct/?$',
        PlannerView.as_view(),
        name="planner_by_facility"),

    # (B):
    url(r'^(?P<facility_slug>[^/]+)/shifts/(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/?$',
        PlannerView.as_view(),
        name="planner_by_facility"),

    # (C):
    url(r'^(?P<facility_slug>[^/]+)/shifts/(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/(?P<shift_id>\d+)/?$',
        ShiftDetailView.as_view(),
        name="shift_details"),


]

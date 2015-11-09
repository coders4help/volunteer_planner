# coding: utf-8

from django.conf.urls import url

from .views import HelpDesk, PlannerView, ShiftDetailView

urlpatterns = [
    url(r'^$', HelpDesk.as_view(), name="helpdesk"),

    url(
        r'^(?P<facility_slug>[^/]+)/shifts/(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/?$',
        PlannerView.as_view(),
        name="planner_by_facility"),

    url(r'^(?P<facility_slug>[^/]+)/shifts/(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/(?P<shift_id>\d+)/?$',
        ShiftDetailView.as_view(), name="shift_details")
]

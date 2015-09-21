# coding: utf-8

from django.conf.urls import url

from .views import HomeView, HelpDesk, PlannerView, get_location_as_json

urlpatterns = [
    url(r'^$', HomeView.as_view(template_name="home.html")),
    url(r'^helpdesk/$', HelpDesk.as_view(), name="helpdesk"),
    url(r'^helpdesk/location/(?P<pk>\d+)/json',
        get_location_as_json,
        name="location_json"),
    url(
        r'^helpdesk/location/(?P<pk>\d+)/(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/$',
        PlannerView.as_view(),
        name="planner_by_location"),
]

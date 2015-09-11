from django.conf.urls import include, url
from django.views.generic import TemplateView
from .views import HomeView, helpdesk, PlannerView, ProfileView, register_for_need, de_register_for_need, volunteer_list, volunteer_checkin_list, checkin_volunteer

urlpatterns = [
    url(r'^$', HomeView.as_view(template_name="home.html")),
    url(r'^helpdesk/$', helpdesk, name="helpdesk"),
    url(r'^helpdesk/location/(?P<pk>\d+)/(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/$', PlannerView.as_view(),
        name="planner_by_location"),
    url(r'^helpdesk/registerforneed/$', register_for_need, name="add_need"),
    url(r'^helpdesk/deregisterforneed/$', de_register_for_need, name="remove_need"),
    url(r'^helpdesk/profile/$', ProfileView.as_view(), name="profile_edit"),
    url(r'^helpdesk/(?P<loc_pk>\d+)/volunteer_list/$', volunteer_list, name="volunteer_list"),
    url(r'^helpdesk/(?P<loc_pk>\d+)/volunteer_checkin_list/$', volunteer_checkin_list, name="volunteer_checkin_list"),
    url(r'^helpdesk/checkin_volunteer/$', checkin_volunteer, name="checkin_volunteer"),
]

# coding=utf-8
from django.conf.urls import url
from django.views.defaults import page_not_found, server_error

from .views import HomeView

urlpatterns = [
    url(r'^$', HomeView.as_view(template_name="home.html"), name="home"),
    url(r'^shelters-need-help/$', HomeView.as_view(template_name="shelters_need_help.html"), name="shelter_info"),
    url(r'^privacy-policy/$', HomeView.as_view(template_name="privacy_policy.html"), name="privacy"),
    url(r'^404/$', page_not_found),
    url(r'^500/$', server_error),
]

# coding=utf-8
from django.urls import re_path
from django.views.defaults import page_not_found, server_error

from .views import HomeView

urlpatterns = [
    re_path(r'^$', HomeView.as_view(template_name="home.html"), name="home"),
    re_path(r'^shelters-need-help/$', HomeView.as_view(template_name="shelters_need_help.html"), name="shelter_info"),
    re_path(r'^privacy-policy/$', HomeView.as_view(template_name="privacy_policy.html"), name="privacy"),
    re_path(r'^404/$', page_not_found),
    re_path(r'^500/$', server_error),
]

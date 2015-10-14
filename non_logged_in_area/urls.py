# coding=utf-8
from django.conf.urls import url

from .views import HomeView

urlpatterns = [
    url(r'^$', HomeView.as_view(template_name="home.html"), name="home"),
    url(r'^shelters-need-help/$', HomeView.as_view(template_name="shelters_need_help.html"), name="shelter_info"),
    url(r'^faqs/$', HomeView.as_view(template_name="faqs.html"), name="faqs"),
    url(r'^privacy-policy/$', HomeView.as_view(template_name="privacy_policy.html"), name="privacy"),
]

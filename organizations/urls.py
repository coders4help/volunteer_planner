# coding: utf-8

from django.conf.urls import url

from .views import shift_management


urlpatterns = [
    url(r'^', shift_management, name="shift_management"),
]

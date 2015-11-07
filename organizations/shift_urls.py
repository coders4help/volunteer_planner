# coding: utf-8

from django.conf.urls import url

from .views import (ShiftManagementView, ShiftDeleteView,
    ShiftCreateView, ShiftUpdateView)


urlpatterns = [
    url(r'^$', ShiftManagementView.as_view(), name="shift_management"),
    url(r'^create/$', ShiftCreateView.as_view(), name="shift_create"),
    url(r'^(?P<pk>\d+)/$', ShiftUpdateView.as_view(), name="shift_update"),
    url(r'^delete/(?P<pk>\d+)/$', ShiftDeleteView.as_view(), name='shift_delete',),
]


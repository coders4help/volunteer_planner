# coding: utf-8

from django.conf.urls import url

from .views import FacilityView

urlpatterns = [
    url(r'^facility/(?P<pk>[^/]+)$', FacilityView.as_view(), name='facility')
]

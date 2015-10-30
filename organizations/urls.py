# coding: utf-8

from django.conf.urls import url
from django.views.generic import TemplateView


from .views import *


urlpatterns = [
    url(r'^shift_delete/([0-9]+)/$', shift_delete, name="shift_delete"),
    url(r'^(?P<id>[0-9]+)/$', ShiftUpdateView.as_view(), name="shift_edit"),
    url(r'^new/$', ShiftCreateView.as_view(), name="shift_new"),
    url(r'^', shift_management, name="shift_management"),
]

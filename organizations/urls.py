# coding: utf-8

from django.conf.urls import url
from django.views.generic import TemplateView


from .views import *


urlpatterns = [
    url(r'^shift_delete/([0-9]+)/$', shift_delete, name="shift_delete"),
    url(r'^edit/([0-9]+)/$', shift_edit, name="shift_edit"),
    url(r'^new/', shift_new, name="shift_new"),
    url(r'^', shift_management, name="shift_management"),
]

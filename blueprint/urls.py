# coding=utf-8
from django.conf.urls import include, url
from django.views.generic import TemplateView
from .views import ExecuteBluePrintView, generate_blueprint

urlpatterns = [
    # Examples:

    url(r'^$', ExecuteBluePrintView.as_view(), name="exec_blueprint"),
    url(r'^generate/', generate_blueprint, name="generate"),

]

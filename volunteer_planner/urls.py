# coding=utf-8
from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView
from content.views import translated_flatpage
from registration.backends.default.views import RegistrationView
from registration.forms import RegistrationFormUniqueEmail

urlpatterns = [
    url(r'^auth/register/$', RegistrationView.as_view(form_class=RegistrationFormUniqueEmail), name='registration_register'),
    url(r'^auth/', include('registration.backends.default.urls')),
    url(r'^account/', include('accounts.urls')),
    url(r'^helpdesk/', include('scheduler.urls')),
    url(r'^orgs/', include('organizations.urls')),
    url(r'^places/', include('scheduler.place_urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^ckeditor/', include('ckeditor.urls')),
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^', include('non_logged_in_area.urls')),
]

urlpatterns += [
    url(r'^(?P<url>.*/)$', translated_flatpage),
]

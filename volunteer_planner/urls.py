# coding=utf-8
from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic import RedirectView

from content.views import translated_flatpage

urlpatterns = [
    # url(r'^auth/', include('registration.backends.admin_approval.urls')),
    url(r'^auth/', include('registration.backends.default.urls')),
    url(r'^account/', include('accounts.urls')),
    url(r'^helpdesk/', include('scheduler.urls')),
    url(r'^orgs/', include('organizations.urls')),
    url(r'^places/', include('scheduler.place_urls')),
    url(r'^admin/uwsgi/', include('django_uwsgi.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^favicon.ico', RedirectView.as_view(url=staticfiles_storage.url('img/favicon.ico'))),
    url(r'^', include('non_logged_in_area.urls')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]

urlpatterns += [
    url(r'^(?P<url>.*/)$', translated_flatpage),
]

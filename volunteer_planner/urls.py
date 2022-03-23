# coding=utf-8
from django.conf import settings
from django.urls import include, re_path
from django.contrib import admin
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic import RedirectView

from content.views import translated_flatpage

urlpatterns = [
    # url(r'^auth/', include('registration.backends.admin_approval.urls')),
    re_path(r'^auth/', include('registration.backends.default.urls')),
    re_path(r'^account/', include('accounts.urls')),
    re_path(r'^helpdesk/', include('scheduler.urls')),
    re_path(r'^orgs/', include('organizations.urls')),
    re_path(r'^places/', include('scheduler.place_urls')),
    re_path(r'^admin/', admin.site.urls),
    re_path(r'^ckeditor/', include('ckeditor_uploader.urls')),
    re_path(r'^i18n/', include('django.conf.urls.i18n')),
    re_path(r'^favicon.ico', RedirectView.as_view(url=staticfiles_storage.url('img/favicon.ico'))),
    re_path(r'^', include('non_logged_in_area.urls')),
]

# if settings.DEBUG:
#     import debug_toolbar
#     urlpatterns += [
#         re_path(r'^__debug__/', include(debug_toolbar.urls)),
#     ]

urlpatterns += [
    re_path(r'^(?P<url>.*/)$', translated_flatpage),
]

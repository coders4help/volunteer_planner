from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView

urlpatterns = [
    # Examples:

    url(r'^auth/', include('registration.backends.default.urls')),
    url(r'^account/', include('accounts.urls')),
    url(r'^faq/', TemplateView.as_view(template_name='faq.html'), name="faq"),
    url(r'^helpdesk/', include('scheduler.urls')),
    url(r'^places/', include('scheduler.place_urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^ckeditor/', include('ckeditor.urls')),
    url(r'^vorlagen/', include('blueprint.urls')),
    url(r'^', include('non_logged_in_area.urls')),
]




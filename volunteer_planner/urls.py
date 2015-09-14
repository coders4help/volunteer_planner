from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView


urlpatterns = [
    # Examples:
    url(r'^auth/', include('registration.urls')),
    url(r'^account/', include('account.urls')),
    url(r'^faq/', TemplateView.as_view(template_name='faq.html'), name="faq"),
    url(r'^', include('scheduler.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^ckeditor/', include('ckeditor.urls')),
    url(r'^vorlagen/', include('blueprint.urls'))
]

from django.conf import settings
from django.contrib.flatpages.models import FlatPage
from django.contrib.flatpages.views import render_flatpage
from django.contrib.sites.shortcuts import get_current_site
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_protect

from content.models import FlatPageTranslation

DEFAULT_TEMPLATE = "flatpages/default.html"


# This view is called from FlatpageFallbackMiddleware.process_response
# when a 404 is raised, which often means CsrfViewMiddleware.process_view
# has not been called even if CsrfViewMiddleware is installed. So we need
# to use @csrf_protect, in case the template needs {% csrf_token %}.
# However, we can't just wrap this view; if no matching flatpage exists,
# or a redirect is required for authentication, the 404 needs to be returned
# without any CSRF checks. Therefore, we only
# CSRF protect the internal implementation.


def translated_flatpage(request, url):
    """
    Public interface to the flat page view.

    Models: `flatpages.flatpages`
    Templates: Uses the template defined by the ``template_name`` field,
        or :template:`flatpages/default.html` if template_name is not defined.
    Context:
        flatpage
            `flatpages.flatpages` object
    """
    if not url.startswith("/"):
        url = f"/{url}"
    site_id = get_current_site(request).id
    try:
        f = get_object_or_404(FlatPage, url=url, sites=site_id)
    except Http404:
        if not url.endswith("/") and settings.APPEND_SLASH:
            url = f"{url}/"
            f = get_object_or_404(FlatPage, url=url, sites=site_id)
        else:
            raise
    return render_translated_flatpage(request, f)


@csrf_protect
def render_translated_flatpage(request, f):
    try:
        translation = f.translations.get(language=request.LANGUAGE_CODE)
        f.title = translation.title
        f.content = translation.content
    except FlatPageTranslation.DoesNotExist:
        print(
            'no translation for page "{flatpage}" for language {lang}'.format(
                flatpage=f.url, lang=request.LANGUAGE_CODE
            )
        )
    return render_flatpage(request, f)

import logging

from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.html import escape
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

logger = logging.getLogger(__name__)


class RedirectOnAdminPermissionDenied403:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        admin_index = reverse("admin:index")
        if (
            hasattr(request, "user")
            and getattr(request.user, "is_authenticated", False)
            and getattr(request.user, "is_staff", False)
            and request.path != admin_index
            and request.path.startswith(admin_index)
            and isinstance(exception, PermissionDenied)
        ):
            redirect_path = admin_index
            error_code = 403
            error = _("Error {error_code}").format(error_code=error_code)
            permission_denied = _("Permission denied")
            error = f"{error}: {permission_denied}"
            note = _(
                "You are not allowed to do this and have been redirected to {redirect_path}."  # noqa: E501
            ).format(redirect_path=redirect_path)
            messages.error(
                request,
                mark_safe(f"<strong>{note}</strong><br/> {error} - ")
                + escape(f"{request.method} {request.path}"),
            )
            return HttpResponseRedirect(redirect_path)

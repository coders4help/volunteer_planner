from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class OrganizationsConfig(AppConfig):
    name = "organizations"
    verbose_name = _("organizations")

    def ready(self):
        # Connect signals
        from . import signals  # noqa

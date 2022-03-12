from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class OrganizationsConfig(AppConfig):
    name = "organizations"
    verbose_name = _("Organizations")

    def ready(self):
        # Connect signals
        from . import signals  # noqa

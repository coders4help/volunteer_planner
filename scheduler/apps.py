# coding=utf-8
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class SchedulerConfig(AppConfig):
    name = 'scheduler'
    verbose_name = _('Scheduler')

    def ready(self):
        # Connect signals
        from . import signals  # noqa

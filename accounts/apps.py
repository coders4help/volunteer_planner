# coding=utf-8
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AccountsConfig(AppConfig):
    name = 'accounts'
    verbose_name = _('Accounts')

    def ready(self):
        import accounts.signals


class RegistrationConfig(AppConfig):
    name = 'registration'
    verbose_name = _('Accounts')

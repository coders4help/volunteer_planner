# coding: utf-8

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from registration.signals import user_activated
from django.dispatch import receiver


class UserAccount(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                related_name='account')

    class Meta:
        verbose_name = _('user account')
        verbose_name_plural = _('user accounts')

@receiver(user_activated)
def registration_completed(sender, user, request, **kwargs):
    account, created = UserAccount.objects.get_or_create(user=user)
    print account, created



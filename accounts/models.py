# coding: utf-8

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _


class UserAccount(models.Model):
    """
    A user account. Used to store any information related to users.
    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                related_name='account')

    class Meta:
        verbose_name = _('user account')
        verbose_name_plural = _('user accounts')

    def __unicode__(self):
        return u'{}'.format(self.user.username)

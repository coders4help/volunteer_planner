# coding: utf-8

from django.db import models
from django.utils.translation import ugettext_lazy as _


class Mailer(models.Model):
    location = models.ForeignKey("scheduler.Location")
    first_name = models.CharField(verbose_name=_("given_name"), max_length=255)
    last_name = models.CharField(verbose_name=_("name"), max_length=255)
    position = models.CharField(verbose_name=_("position"), max_length=255)
    organization = models.CharField(verbose_name=_("organisation"), max_length=255)
    email = models.EmailField(verbose_name=_("email"))

    def __unicode__(self):
        return u'{} ({})'.format(self.organization, self.location.name)

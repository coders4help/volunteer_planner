# coding: utf-8

from django.db import models
from django.utils.translation import gettext_lazy as _


class Mailer(models.Model):
    facility = models.ForeignKey("organizations.Facility", models.CASCADE)
    first_name = models.CharField(verbose_name=_("first name"), max_length=255)
    last_name = models.CharField(verbose_name=_("last name"), max_length=255)
    position = models.CharField(verbose_name=_("position"), max_length=255)
    organization = models.CharField(verbose_name=_("organisation"), max_length=255)
    email = models.EmailField(verbose_name=_("email"))

    def __unicode__(self):
        return u'{} ({})'.format(self.organization, self.facility.name)

    def __str__(self):
        return self.__unicode__()

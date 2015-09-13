# coding: utf-8

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import slugify


class Notification(models.Model):
    """
    News updates/"Aufrufe" from locations. Displayed where relevant.
    """
    creation_date = models.DateField(auto_now=True)
    title = models.CharField(max_length=255, verbose_name=_("title"))
    subtitle = models.CharField(max_length=255, verbose_name=_("subtitle"), null=True, blank=True)
    text = models.TextField(max_length=20055, verbose_name=_("articletext"))
    slug = models.SlugField(auto_created=True, max_length=255)
    location = models.ForeignKey('scheduler.Location')

    def save(self, *args, **kwargs):
        if not self.id:
            # Newly created object, so set slug
            self.slug = slugify(self.title)

        super(Notification, self).save(*args, **kwargs)

    def __unicode__(self):
        return u'{}'.format(self.title)

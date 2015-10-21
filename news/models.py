# coding: utf-8

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import slugify


class News(models.Model):
    """
    facilities and organizations can publish news.
    TODO: News are shown in appropriate organization templates
    """
    creation_date = models.DateField(auto_now=True, verbose_name=_("creation date"))
    title = models.CharField(max_length=255, verbose_name=_("title"))
    subtitle = models.CharField(max_length=255, verbose_name=_("subtitle"), null=True, blank=True)
    text = models.TextField(max_length=20055, verbose_name=_("articletext"))
    slug = models.SlugField(auto_created=True, max_length=255)
    facility = models.ForeignKey('organizations.Facility', null=True, blank=True)
    organization = models.ForeignKey('organizations.Organization', null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.id:
            # Newly created object, so set slug
            self.slug = slugify(self.title)

        super(News, self).save(*args, **kwargs)

    def __unicode__(self):
        return u'{}'.format(self.title)

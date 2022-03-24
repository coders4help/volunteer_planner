# coding: utf-8

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.template.defaultfilters import slugify


class NewsEntry(models.Model):
    """
    facilities and organizations can publish news.
    TODO: News are shown in appropriate organization templates
    """
    title = models.CharField(max_length=255,
                             verbose_name=_("title"))

    subtitle = models.CharField(max_length=255,
                                verbose_name=_("subtitle"),
                                null=True,
                                blank=True)

    text = models.TextField(verbose_name=_("articletext"))

    slug = models.SlugField(auto_created=True, max_length=255)

    creation_date = models.DateField(auto_now=True,
                                     verbose_name=_("creation date"))

    facility = models.ForeignKey('organizations.Facility',
                                 models.CASCADE,
                                 related_name='news_entries',
                                 null=True,
                                 blank=True)

    organization = models.ForeignKey('organizations.Organization',
                                     models.CASCADE,
                                     related_name='news_entries',
                                     null=True,
                                     blank=True)

    class Meta:
        verbose_name = _('news entry')
        verbose_name_plural = _('news entries')
        ordering = ('facility', 'organization', 'creation_date')

    def save(self, *args, **kwargs):
        if not self.id:
            # Newly created object, so set slug
            self.slug = slugify(self.title)
        super(NewsEntry, self).save(*args, **kwargs)

    def __unicode__(self):
        return u'{}'.format(self.title)

    def __str__(self):
        return self.__unicode__()

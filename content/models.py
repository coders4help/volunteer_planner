# coding: utf-8

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.contrib.flatpages.models import FlatPage


class FlatPageExtraStyle(models.Model):
    flatpage = models.OneToOneField(FlatPage,
                                    models.CASCADE,
                                    related_name='extra_style',
                                    verbose_name=_('additional style'),
                                    )

    css = models.TextField(_('additional CSS'), blank=True)

    class Meta:
        verbose_name = _('additional flat page style')
        verbose_name_plural = _('additional flat page styles')


class FlatPageTranslation(models.Model):
    flatpage = models.ForeignKey(FlatPage,
                                 models.CASCADE,
                                 related_name='translations',
                                 verbose_name=_('flat page'),
                                 )

    language = models.CharField(_('language'),
                                max_length=20,
                                choices=settings.LANGUAGES)

    title = models.CharField(_('title'),
                             max_length=200,
                             blank=True)

    content = models.TextField(_('content'),
                               blank=True)

    def save(self, *args, **kwargs):
        if not self.title:
            self.title = self.flatpage.title
        super(FlatPageTranslation, self).save(*args, **kwargs)

    class Meta:
        unique_together = ('flatpage', 'language')
        verbose_name = _('flat page translation')
        verbose_name_plural = _('flat page translations')

# coding: utf-8

from datetime import timedelta

from django.db import models
from django.utils import timezone
from django.utils.formats import localize
from django.utils.translation import ugettext_lazy as _

from organizations.models import Facility
from places.models import Country, Region, Area, Place


class NeedManager(models.Manager):
    def at_facility(self, facility):
        return self.get_queryset().filter(facility=facility)

    def at_place(self, place):
        return self.get_queryset().filter(facility__place=place)

    def in_area(self, area):
        return self.get_queryset().filter(facility__place__area=area)

    def in_region(self, region):
        return self.get_queryset().filter(facility__place__area__region=region)

    def in_country(self, country):
        return self.get_queryset().filter(
            facility__place__area__region__country=country)

    def by_geography(self, geo_affiliation):
        if isinstance(geo_affiliation, Facility):
            return self.at_facility(geo_affiliation)
        elif isinstance(geo_affiliation, Place):
            return self.at_place(geo_affiliation)
        elif isinstance(geo_affiliation, Area):
            return self.in_area(geo_affiliation)
        elif isinstance(geo_affiliation, Region):
            return self.in_region(geo_affiliation)
        elif isinstance(geo_affiliation, Country):
            return self.in_country(geo_affiliation)


class OpenNeedManager(NeedManager):
    def get_queryset(self):
        now = timezone.now()
        qs = super(OpenNeedManager, self).get_queryset()
        return qs.filter(ending_time__gte=now)


class Need(models.Model):
    """
    This is the primary instance to create shifts
    """

    topic = models.ForeignKey("Topics", verbose_name=_(u'help type'),
                              help_text=_(u'HELP_TYPE_HELP'))

    facility = models.ForeignKey('organizations.Facility',
                                 verbose_name=_(u'facility'))

    starting_time = models.DateTimeField(verbose_name=_('starting time'),
                                         db_index=True)
    ending_time = models.DateTimeField(verbose_name=_('ending time'),
                                       db_index=True)

    helpers = models.ManyToManyField('accounts.UserAccount',
                                     through='ShiftHelper',
                                     related_name='needs')

    # Currently required. If you want to allow not setting this, make sure to update
    # associated logic where slots is used.
    slots = models.IntegerField(verbose_name=_(u'number of needed volunteers'))

    objects = NeedManager()
    open_needs = OpenNeedManager()

    class Meta:
        verbose_name = _(u'shift')
        verbose_name_plural = _(u'shifts')
        ordering = ['starting_time', 'ending_time']

    def __unicode__(self):
        return u"{title} - {facility} ({start} - {end})".format(
            title=self.topic.title, facility=self.facility.name,
            start=localize(self.starting_time), end=localize(self.ending_time))


class ShiftHelperManager(models.Manager):
    def conflicting(self, need, user_account=None, grace=timedelta(hours=1)):

        grace = grace or timedelta(0)
        graced_start = need.starting_time + grace
        graced_end = need.ending_time - grace

        query_set = self.get_queryset().select_related('need', 'user_account')

        if user_account:
            query_set = query_set.filter(user_account=user_account)

        query_set = query_set.exclude(need__starting_time__lt=graced_start,
                                      need__ending_time__lte=graced_start)
        query_set = query_set.exclude(need__starting_time__gte=graced_end,
                                      need__ending_time__gte=graced_end)
        return query_set


class ShiftHelper(models.Model):
    user_account = models.ForeignKey('accounts.UserAccount',
                                     related_name='shift_helpers')
    need = models.ForeignKey('scheduler.Need', related_name='shift_helpers')
    joined_shift_at = models.DateTimeField(auto_now_add=True)

    objects = ShiftHelperManager()

    class Meta:
        verbose_name = _('shift helper')
        verbose_name_plural = _('shift helpers')
        unique_together = ('user_account', 'need')

    def __repr__(self):
        return "{}".format(self.need)

    def __unicode__(self):
        return u"{}".format(repr(self))


class Topics(models.Model):
    class Meta:
        verbose_name = _(u'help type')
        verbose_name_plural = _(u'help types')

    title = models.CharField(max_length=255)
    description = models.TextField(max_length=20000, blank=True)

    def __unicode__(self):
        return self.title

    def get_current_needs_py_topic(self):
        return self.need_set.all()


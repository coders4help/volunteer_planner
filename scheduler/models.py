# coding: utf-8

import datetime
import locale

from django.db import models
from django.utils.formats import localize
from django.utils.translation import ugettext_lazy as _


class Need(models.Model):
    """
    This is the primary instance to create shifts
    """

    class Meta:
        verbose_name = _(u'shift')
        verbose_name_plural = _(u'shifts')

    topic = models.ForeignKey("Topics", verbose_name=_(u'helptype'), help_text=_(u'helptype_text'))
    location = models.ForeignKey('Location', verbose_name=_(u'location'))

    starting_time = models.DateTimeField(verbose_name=_('starting time'))
    ending_time = models.DateTimeField(verbose_name=_('ending time'))

    # Currently required. If you want to allow not setting this, make sure to update
    # associated logic where slots is used.
    slots = models.IntegerField(verbose_name=_(u'number of needed volunteers'))

    def get_conflicting_needs(self, needs, grace=datetime.timedelta(hours=1)):
        """
        Given a list of other needs, this function returns needs that overlap by time.
        A grace period of overlap is allowed:

               Event A: 10 till 14
               Event B: 13 till 15

        would not conflict if a grace period of 1 hour or more is allowed, but would conflict if
        the grace period is less.

        This is not the most efficient implementation, but one of the more obvious. Optimize
        only if needed. Nicked from:
        http://stackoverflow.com/questions/3721249/python-date-interval-intersection

        :param needs: A Django queryset of Need instances.
        """
        latest_start_time = self.starting_time + grace
        earliest_end_time = self.ending_time - grace
        if earliest_end_time <= latest_start_time:
            # Event is shorter than 2 * grace time, can't have overlaps.
            return []

        return [
            need for need in needs
            if (need.starting_time < latest_start_time < need.ending_time) or
            (latest_start_time < need.starting_time < earliest_end_time)
            ]

    def __unicode__(self):
        return u"{title} - {location} ({start} - {end})".format(
            title=self.topic.title, location=self.location.name,
            start=localize(self.starting_time), end=localize(self.ending_time))


class Topics(models.Model):
    class Meta:
        verbose_name = _(u'helptype')
        verbose_name_plural = _(u'helptypes')

    title = models.CharField(max_length=255)
    description = models.TextField(max_length=20000, blank=True)

    def __unicode__(self):
        return self.title

    def get_current_needs_py_topic(self):
        return self.need_set.all()


class Location(models.Model):
    name = models.CharField(max_length=255, blank=True)
    street = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=255, blank=True)
    postal_code = models.CharField(max_length=5, blank=True)
    latitude = models.CharField(max_length=30, blank=True)
    longitude = models.CharField(max_length=30, blank=True)
    additional_info = models.TextField(max_length=300000, blank=True)

    class Meta:
        verbose_name = _(u'location')
        verbose_name_plural = _(u'locations')
        permissions = (
            ("can_view", u"User can view location"),
        )

    def __unicode__(self):
        return u'{}'.format(self.name)

    def get_dates_of_needs(self):
        needs_dates = []
        for i in self.need_set.all().filter(ending_time__gt=datetime.datetime.now()) \
                .order_by('ending_time'):
            date_name = i.starting_time.strftime("%A, %d.%m.%Y")
            locale.setlocale(locale.LC_ALL, 'de_DE.UTF-8')
            if date_name not in needs_dates:
                needs_dates.append(i.starting_time.strftime("%A, %d.%m.%Y"))
        return needs_dates

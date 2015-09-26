# coding: utf-8

import datetime

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

    topic = models.ForeignKey("Topics", verbose_name=_(u'help type'),
                              help_text=_(u'HELP_TYPE_HELP'))
    location = models.ForeignKey('Location', verbose_name=_(u'location'))

    starting_time = models.DateTimeField(verbose_name=_('starting time'),
                                         db_index=True)
    ending_time = models.DateTimeField(verbose_name=_('ending time'),
                                       db_index=True)

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
        verbose_name = _(u'help type')
        verbose_name_plural = _(u'help types')

    title = models.CharField(max_length=255)
    description = models.TextField(max_length=20000, blank=True)

    def __unicode__(self):
        return self.title

    def get_current_needs_py_topic(self):
        return self.need_set.all()


class Location(models.Model):
    name = models.CharField(max_length=255, blank=True,
                            verbose_name=_('name'))
    street = models.CharField(max_length=255, blank=True,
                              verbose_name=_('address'))
    city = models.CharField(max_length=255, blank=True,
                            verbose_name=_('city'))
    postal_code = models.CharField(max_length=5, blank=True,
                                   verbose_name=_('postal code'))
    latitude = models.CharField(max_length=30, blank=True,
                                verbose_name=_('latitude'))
    longitude = models.CharField(max_length=30, blank=True,
                                 verbose_name=_('longitude'))
    additional_info = models.TextField(max_length=300000, blank=True,
                                       verbose_name=_('description'))

    place = models.ForeignKey("places.Place",
                              null=False,
                              related_name='locations',
                              verbose_name=_('place'))

    class Meta:
        verbose_name = _(u'location')
        verbose_name_plural = _(u'locations')
        ordering = ('place', 'name', )
        permissions = (
            ("can_view", u"User can view location"),
        )

    def __unicode__(self):
        return u'{}'.format(self.name)


# class Organization(models.Model):
#     '''
#     An organization is a NGO or a group of people managing one or more facilities.
#     '''
#     name = models.CharField(max_length=50, unique=True, verbose_name=_('name'))
#     description = models.TextField(null=True, blank=True, verbose_name=_('description'))
#     slug = models.SlugField(verbose_name=_(u'slug'))
#
#     class Meta:
#         verbose_name = _('organization')
#         verbose_name_plural = _('organizations')
#         ordering = ('name',)
#
#     def __str__(self):
#         return '{}'.format(self.name)


class WorkDone(models.Model):
    """
    A SQL view is used to calculate total volunteer hours. This unmanaged model is used to
    let us access that data via Django.

    Note that this won't work with a local SQLite backend.
    """
    id = models.IntegerField(primary_key=True)
    hours = models.IntegerField(name=u'hours', verbose_name=_('working hours'))

    class Meta:
        managed = False
        db_table = 'work_done'

    def __unicode__(self):
        return u'{}'.format(self.hours)

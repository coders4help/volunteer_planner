# coding: utf-8
from datetime import time

from django.db import models
from django.utils.formats import localize
from django.utils.translation import ugettext_lazy as _, ungettext_lazy

from places.models import Country, Region, Area, Place
from . import managers


class Shift(models.Model):
    """
    This is the primary instance to create shifts
    """

    slots = models.IntegerField(verbose_name=_(u'number of needed volunteers'))

    task = models.ForeignKey("organizations.Task",
                             verbose_name=_(u'task'))
    workplace = models.ForeignKey("organizations.Workplace",
                                  verbose_name=_(u'workplace'),
                                  null=True,
                                  blank=True)

    facility = models.ForeignKey('organizations.Facility',
                                 verbose_name=_(u'facility'))

    starting_time = models.DateTimeField(verbose_name=_('starting time'),
                                         db_index=True)
    ending_time = models.DateTimeField(verbose_name=_('ending time'),
                                       db_index=True)

    helpers = models.ManyToManyField('accounts.UserAccount',
                                     through='ShiftHelper',
                                     related_name='shifts')

    members_only = models.BooleanField(default=False,
                                       verbose_name=_(u'members only'),
                                       help_text=_(
                                           u'allow only members to help'))

    objects = managers.ShiftManager()
    open_shifts = managers.OpenShiftManager()

    class Meta:
        verbose_name = _(u'shift')
        verbose_name_plural = _(u'shifts')
        ordering = ['starting_time', 'ending_time']

    @property
    def days(self):
        return (self.ending_time.date() - self.starting_time.date()).days

    @property
    def duration(self):
        return self.ending_time - self.starting_time

    @property
    def localized_display_ending_time(self):
        days = self.days if self.ending_time.time() > time.min else 0
        days_fmt = ungettext_lazy(u'the next day',
                                  u'after {number_of_days} days',
                                  days)
        days_str = days_fmt.format(number_of_days=days) if days else u''
        return u'{time} {days}'.format(time=localize(self.ending_time.time()),
                                       days=days_str).strip()

    def __unicode__(self):
        return u"{title} - {facility} ({start} - {end})".format(
            title=self.task.name,
            facility=self.facility.name,
            start=localize(self.starting_time),
            end=localize(self.ending_time))


class ShiftHelper(models.Model):
    user_account = models.ForeignKey('accounts.UserAccount',
                                     related_name='shift_helpers')
    shift = models.ForeignKey('scheduler.Shift', related_name='shift_helpers')
    joined_shift_at = models.DateTimeField(auto_now_add=True)

    objects = managers.ShiftHelperManager()

    class Meta:
        verbose_name = _('shift helper')
        verbose_name_plural = _('shift helpers')
        unique_together = ('user_account', 'shift')

    def __unicode__(self):
        return u"{} on {}".format(self.user_account.user.username,
                                  self.shift.task)

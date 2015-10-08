# coding: utf-8

from django.db import models
from django.utils.formats import localize
from django.utils.translation import ugettext_lazy as _

from organizations.models import Facility
from places.models import Country, Region, Area, Place
from . import old_managers


# old models

class Topics(models.Model):
    class Meta:
        verbose_name = _(u'help type')
        verbose_name_plural = _(u'help types')

    title = models.CharField(max_length=255)
    description = models.TextField(max_length=20000, blank=True)
    workplace = models.CharField(max_length=255, blank=True,
                                 verbose_name=_('workplace'))

    def __unicode__(self):
        return u'{}'.format(self.title)

    def get_current_needs_py_topic(self):
        return self.need_set.all()


class Need(models.Model):
    """
    This is the primary instance to create shifts
    """

    topic = models.ForeignKey("Topics", verbose_name=_(u'help type'),
                              help_text=_(u'HELP_TYPE_HELP'))

    facility = models.ForeignKey('organizations.Facility',
                                 verbose_name=_(u'facility'),
                                 null=True)

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

    objects = old_managers.NeedManager()
    open_needs = old_managers.OpenNeedManager()

    class Meta:
        verbose_name = _(u'shift')
        verbose_name_plural = _(u'shifts')
        ordering = ['starting_time', 'ending_time']

    def __unicode__(self):
        return u"{title} - {facility} ({start} - {end})".format(
            title=self.topic.title, facility=self.facility.name,
            start=localize(self.starting_time), end=localize(self.ending_time))


class ShiftHelper(models.Model):
    user_account = models.ForeignKey('accounts.UserAccount',
                                     related_name='shift_helpers')
    need = models.ForeignKey('scheduler.Need', related_name='shift_helpers')
    joined_shift_at = models.DateTimeField(auto_now_add=True)

    objects = old_managers.ShiftHelperManager()

    class Meta:
        verbose_name = _('shift helper')
        verbose_name_plural = _('shift helpers')
        unique_together = ('user_account', 'need')

    def __unicode__(self):
        return u"{} on {}".format(self.user_account.user.username,
                                  self.need.topic)

# New models

# class Shift(models.Model):
#     """
#     A shift. Happens at a time and place, and hopefully has many volunteers attached to it.
#     """
#     task = models.ForeignKey("organizations.Task", verbose_name=_(u'task'),
#                              help_text=_(u''))
#     workplace = models.ForeignKey("organizations.Workplace",
#                                   verbose_name=_(u'workplace'),
#                                   help_text=_(u''))
#     volunteers = models.ManyToManyField(
#         'accounts.UserAccount', through='scheduler.Enrolment',
#         related_name='shifts', verbose_name=_('volunteers'))
#     # to set only if created from template. But really useful? Maybe just more complexity
#     # origin_event = models.ForeignKey("RecurringEvent", null=True, verbose_name=_(u''), help_text=_(u''))
#     needed_volunteers = models.IntegerField(
#         verbose_name=_(u'number of needed volunteers'))
#     start_time = models.DateTimeField(verbose_name=_('starting time'),
#                                       db_index=True)
#     end_time = models.DateTimeField(verbose_name=_('ending time'),
#                                     db_index=True)
#
#     objects = managers.ShiftManager()
#
#     def __unicode__(self):
#         return _(u"{} at {}").format(self.task, self.workplace)
#
#
# class Enrolment(models.Model):
#     """
#     Through model, representing when a user enrolled for a shift.
#     """
#     user_account = models.ForeignKey('accounts.UserAccount',
#                                      related_name='enrolments',
#                                      verbose_name=_('user account'))
#     shift = models.ForeignKey('scheduler.Shift',
#                               related_name='enrolled_users',
#                               verbose_name=_('shift'))
#     joined_shift_at = models.DateTimeField(auto_now_add=True,
#                                            verbose_name=_('joined at'))
#
#     objects = managers.EnrolmentManager()
#
#     class Meta:
#         verbose_name = _('Enrolment for shift')
#         verbose_name_plural = _('Enrolments for shifts')
#         unique_together = ('user_account', 'shift')
#
#     def __unicode__(self):
#         return _(u"{} on {}").format(self.user, self.shift)
#
#
# class RecurringEvent(models.Model):
#     """
#     A sort of blueprint to bulk-create shifts.
#     """
#     WEEKDAYS = ((0, _('Monday')),
#                 (1, _('Tuesday')),
#                 (2, _('Wednesday')),
#                 (3, _('Thursday')),
#                 (4, _('Friday')),
#                 (5, _('Saturday')),
#                 (6, _('Sunday')))
#     task = models.ForeignKey("organizations.Task", verbose_name=_('task'))
#     workplace = models.ForeignKey("organizations.Workplace",
#                                   verbose_name=_('workplace'))
#     name = models.CharField(max_length=255, verbose_name=_('name'))
#     description = models.TextField(blank=True, verbose_name=_('description'))
#     weekday = models.IntegerField(choices=WEEKDAYS, verbose_name=_('weekday'))
#     needed_volunteers = models.IntegerField(
#         verbose_name=_(u'number of needed volunteers'))
#     start_time = models.TimeField(verbose_name=_('Starting time'))
#     end_time = models.TimeField(verbose_name=_('Ending time'))
#     first_date = models.DateTimeField(verbose_name=_('First occurrence'))
#     last_date = models.DateTimeField(verbose_name=_('Last occurrence'))
#
#     disabled = models.BooleanField(verbose_name=_('Disabled'), default=False)
#
#     objects = managers.RecurringEventManager()
#
#     def __unicode__(self):
#         return _(u"{}").format(self.name)

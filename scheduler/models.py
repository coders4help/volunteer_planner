# coding: utf-8

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.formats import localize

from django.utils.translation import ugettext_lazy as _

from . import managers


## KEPT FROM OLD FOR NEW MODEL

class Location(models.Model):
    """
    TODO:
    * Name, street, city, postal_code probably shouldn't be blank
    * This really is a container for an address; it should be called that.
    * lat/long should be removed until needed. Needs timestamps for last address
      update and last lat/long update to be useful.
    * Should be moved to places app
    """
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
        ordering = ('place', 'name',)
        permissions = (
            ("can_view", u"User can view location"),
        )

    def __unicode__(self):
        return self.name


## OLD PART TO BE REMOVED LATER


class Need(models.Model):
    """
    This is the primary instance to create shifts
    """

    topic = models.ForeignKey("Topics", verbose_name=_(u'help type'),
                              help_text=_(u'HELP_TYPE_HELP'))
    location = models.ForeignKey('Location', verbose_name=_(u'location'))

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

    objects = managers.NeedManager()
    open_needs = managers.OpenNeedManager()

    class Meta:
        verbose_name = _(u'shift')
        verbose_name_plural = _(u'shifts')
        ordering = ['starting_time', 'ending_time']

    def __unicode__(self):
        return u"{title} - {location} ({start} - {end})".format(
            title=self.topic.title, location=self.location.name,
            start=localize(self.starting_time), end=localize(self.ending_time))


class ShiftHelper(models.Model):
    user_account = models.ForeignKey('accounts.UserAccount',
                                     related_name='shift_helpers')
    need = models.ForeignKey('scheduler.Need', related_name='shift_helpers')
    joined_shift_at = models.DateTimeField(auto_now_add=True)

    objects = managers.ShiftHelperManager()

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

### NEW PART


class Enrolment(models.Model):
    """
    Through model, representing when a user enrolled for a shift.
    """
    user = models.ForeignKey('accounts.UserAccount')
    shift = models.ForeignKey('scheduler.Shift')
    joined_shift_at = models.DateTimeField(auto_now_add=True)

    objects = managers.EnrolmentManager()

    class Meta:
        verbose_name = _('Enrolment for shift')
        verbose_name_plural = _('Enrolments for shifts')
        unique_together = ('user', 'shift')

    def __unicode__(self):
        return _(u"{} enrolment for").format(self.user, self.shift)


# TBD: Isn't this too fine-grained? Maik would leave it out till we're sure we need it.
#
# class Skill(models.Model):
#     """
#     A particular skill of an individual, like cooking or translating.
#     """
#     name = models.CharField(max_length=255)
#     description = models.TextField(blank=True)
#     needs_approval = models.BooleanField(verbose_name=_(u'Skill needs approval'))


class Task(models.Model):
    """
    A particular task to be performed, like taking care of kids.
    """
    #skill = models.ManyToManyField("scheduler.Skill", verbose_name=_(u''), help_text=_(u''))
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)


class RecurringEvent(models.Model):
    """
    A sort of blueprint to bulk-create shifts.
    """
    WEEKDAYS = ((0, _('Monday')),
                (1, _('Tuesday')),
                (2, _('Wednesday')),
                (3, _('Thursday')),
                (4, _('Friday')),
                (5, _('Saturday')),
                (6, _('Sunday')))
    task = models.ForeignKey("scheduler.Task")
    workplace = models.ForeignKey("places.Workplace")
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    weekday = models.IntegerField(choices=WEEKDAYS)
    needed_volunteers = models.IntegerField(verbose_name=_(u'number of needed volunteers'))
    start_time = models.TimeField(verbose_name=_('Starting time'))
    end_time = models.TimeField(verbose_name=_('Ending time'))
    first_date = models.DateTimeField(verbose_name=_('First occurrence'))
    last_date = models.DateTimeField(verbose_name=_('Last occurrence'))
    created_at = models.DateTimeField(verbose_name=_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name=_('updated at'), auto_now=True)
    disabled = models.BooleanField(verbose_name=_('Disabled'), default=False)

    objects = managers.RecurringEventManager()


class Shift(models.Model):
    """
    A shift. Happens at a time and place, and hopefully has many volunteers attached to it.
    """
    task = models.ForeignKey("scheduler.Task", verbose_name=_(u''), help_text=_(u''))
    workplace = models.ForeignKey("places.Workplace", verbose_name=_(u''), help_text=_(u''))
    volunteers = models.ManyToManyField(
        'accounts.UserAccount', through='scheduler.Enrolment', related_name='shifts')
    # to set only if created from template. But really useful? Maybe just more complexity
    # origin_event = models.ForeignKey("RecurringEvent", null=True, verbose_name=_(u''), help_text=_(u''))
    needed_volunteers = models.IntegerField(verbose_name=_(u'number of needed volunteers'))
    start_time = models.DateTimeField(verbose_name=_('starting time'), db_index=True)
    end_time = models.DateTimeField(verbose_name=_('ending time'), db_index=True)
    created_at = models.DateTimeField(verbose_name=_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name=_('updated at'), auto_now=True)
    published_at = models.DateTimeField(verbose_name=_('published at'), null=True)
    cancelled_at = models.DateTimeField(verbose_name=_('cancelled at'), null=True)

    objects = managers.ShiftManager()

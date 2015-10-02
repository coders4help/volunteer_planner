# coding: utf-8

from datetime import timedelta
from dateutil.parser import parse
from django.core.exceptions import ValidationError

from django.db import models
from django.utils import timezone
from django.utils.formats import localize
from django.utils.translation import ugettext_lazy as _

from places.models import Country, Area, Place
from places.models import Region


## KEPT FROM OLD FOR NEW MODEL

class NeedManager(models.Manager):
    def at_location(self, location):
        return self.get_queryset().filter(location=location)

    def at_place(self, place):
        return self.get_queryset().filter(location__place=place)

    def in_area(self, area):
        return self.get_queryset().filter(location__place__area=area)

    def in_region(self, region):
        return self.get_queryset().filter(location__place__area__region=region)

    def in_country(self, country):
        return self.get_queryset().filter(
            location__place__area__region__country=country)

    def by_geography(self, geo_affiliation):
        if isinstance(geo_affiliation, Location):
            return self.at_location(geo_affiliation)
        elif isinstance(geo_affiliation, Place):
            return self.at_place(geo_affiliation)
        elif isinstance(geo_affiliation, Area):
            return self.in_area(geo_affiliation)
        elif isinstance(geo_affiliation, Region):
            return self.in_region(geo_affiliation)
        elif isinstance(geo_affiliation, Country):
            return self.in_country(geo_affiliation)



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
        ordering = ('place', 'name',)
        permissions = (
            ("can_view", u"User can view location"),
        )

    def __unicode__(self):
        return u'{}'.format(self.name)


## OLD PART TO BE REMOVED LATER

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

    objects = NeedManager()
    open_needs = OpenNeedManager()

    class Meta:
        verbose_name = _(u'shift')
        verbose_name_plural = _(u'shifts')
        ordering = ['starting_time', 'ending_time']

    def __unicode__(self):
        return u"{title} - {location} ({start} - {end})".format(
            title=self.topic.title, location=self.location.name,
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

### NEW PART

class ShiftRegistrationManager(models.Manager):
    def conflicting(self, shift, user_account=None, grace=timedelta(hours=1)):

        grace = grace or timedelta(0)
        graced_start = shift.starting_time + grace
        graced_end = shift.ending_time - grace

        query_set = self.get_queryset().select_related('shift', 'user_account')

        if user_account:
            query_set = query_set.filter(user_account=user_account)

        query_set = query_set.exclude(shift__start_time__lt=graced_start,
                                      shift__end_time__lte=graced_start)
        query_set = query_set.exclude(shift__start_time__gte=graced_end,
                                      shift__end_time__gte=graced_end)
        return query_set


class ShiftRegistration(models.Model):
    user_account = models.ForeignKey('accounts.UserAccount')
    shift = models.ForeignKey('scheduler.Shift')
    joined_shift_at = models.DateTimeField(auto_now_add=True)
    registration_ip = models.GenericIPAddressField()

    objects = ShiftRegistrationManager()

    class Meta:
        verbose_name = _('shift registration')
        verbose_name_plural = _('shift registrations')
        unique_together = ('user_account', 'shift')

    def __repr__(self):
        return "{}".format(self.shift)

    def __unicode__(self):
        return u"{}".format(repr(self))


class Skill(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=20000, blank=True)
    needs_approval = models.BooleanField(verbose_name=_(u'Skill needs approval'))


class Task(models.Model):
    skill = models.ManyToManyField("scheduler.Skill", verbose_name=_(u''), help_text=_(u''))
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=20000, blank=True)


class Workplace(models.Model):
    facility = models.ForeignKey("TBD.Facility", verbose_name=_(u''), help_text=_(u''))
    # set only location if different from facility?
    location = models.ForeignKey("scheduler.Location", null=True, verbose_name=_(u''), help_text=_(u''))
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=20000, blank=True)

# TODO: Think about timezone!
# Blueprint is replaced by this. Day occurrence adjustment/copy is done on front-end
# slot_amount is here an integer to make queries faster, it could evolve to something more flexible
# or have something like senior_amount of manager_amount later on

def time_validator(value):
    if len(value) != 5:
        raise ValidationError('length of %s is not equal to 5' % value)
    if value[2] != ':':
        raise ValidationError('separator of %s is not ":"' % value)
    hours, minutes = value.split(':')
    try:
        hours = int(hours)
        minutes = int(minutes)
    except Exception, e:
        raise ValidationError('hours and minutes of %s can not be converted to integer' % value)
    if hours < 0 or hours > 23:
        raise ValidationError('hours %s can not be lower than 0 or higher than 23' % value)
    if minutes < 0 or minutes > 59:
        raise ValidationError('minutes %s can not be lower than 0 or higher than 59' % value)


class RecurringEventManager(models.Manager):

    def get_events_for_facility_and_day(self, facility, day):
        weekday = day.weekday()
        # since working with datetime, we may need to add deltatime and so here
        return self.filter(facility=facility,
                           weekday=weekday,
                           first_date__gte=day,
                           end_date__lte=day,
                           disabled=False)


class RecurringEvent(models.Model):
    WEEKDAYS = ((0, _('Monday')),
                (1, _('Tuesday')),
                (2, _('Wednesday')),
                (3, _('Thursday')),
                (4, _('Friday')),
                (5, _('Saturday')),
                (6, _('Sunday')))
    facility = models.ForeignKey("TBD.Facility", verbose_name=_(u''), help_text=_(u''))
    task = models.ForeignKey("scheduler.Task", verbose_name=_(u''), help_text=_(u''))
    workplace = models.ForeignKey("scheduler.Workplace", verbose_name=_(u''), help_text=_(u''))
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=20000, blank=True)
    weekday = models.IntegerField(choices=WEEKDAYS, null=False)
    slot_amount = models.IntegerField(verbose_name=_(u'number of needed volunteers'))
    start_time = models.CharField(verbose_name=_('Starting time'), max_length=5, validators=[time_validator])
    end_time = models.CharField(verbose_name=_('Ending time'), max_length=5)
    first_date = models.DateTimeField(verbose_name=_('First occurence'))
    last_date = models.DateTimeField(verbose_name=_('Last occurence'))
    created_at = models.DateTimeField(verbose_name=_('created_at'), auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name=_('updated_at'), auto_now=True)
    disabled = models.BooleanField(verbose_name=_('Disabled'), default=False)
    # Event slug as well as any other grouping mechanism is disabled for now, to be added on request later on
    # event_slug = models.CharField(max_length=255)

    objects = RecurringEventManager()

    # @property
    # def slugify(self):
    #     return '{}#{}-{}'.format(self.weekday, self.start_time, self.end_time)

    def save(self, *args, **kwargs):
        # TODO: special checks for start_time and end_time CharField? in a validate method? Subclass of CharField?
        #self.event_slug = self.slugify
        self.save(*args, **kwargs)


# This "second" view allows to create/publish the shifts for the X coming days out of the recurring events
# On REST side, it should be possible to request all events from the template for a specified day,
# return them to the front-end which will publish them and/or modify them via PUTs statements

class ShiftManager(NeedManager):

    def create_datetime_from_day_and_time_string(self, day, time_str):
        return parse(time_str, default=day)

    def create_shift_from_event_and_day(self, event, day):
        shift = Shift(facility=event.facility,
                      task=event.task,
                      workplace=event.workplace,
                      name=event.name,
                      description=event.description,
                      slot_amount=event.slot_amount,
                      start_time=self.create_datetime_from_day_and_time_string(day, event.start_time),
                      end_time=self.create_datetime_from_day_and_time_string(day, event.end_time))
        # shift.save() # see if it should be done here later
        return shift

    def create_shifts_for_facility_and_day(self, facility, day):
        events = RecurringEvent.objects.get_events_for_facility_and_day(facility, day)
        shifts = []
        for event in events:
            shifts.append(self.create_shift_from_event_and_day(event, day))
        return shifts


class OpenShiftManager(ShiftManager):
    def get_queryset(self):
        now = timezone.now()
        qs = super(OpenShiftManager, self).get_queryset()
        return qs.filter(end_time__gte=now)


class Shift(models.Model):
    facility = models.ForeignKey("TBD.Facility", verbose_name=_(u''), help_text=_(u''))
    task = models.ForeignKey("scheduler.Task", verbose_name=_(u''), help_text=_(u''))
    workplace = models.ForeignKey("scheduler.Workplace", verbose_name=_(u''), help_text=_(u''))
    helpers = models.ManyToManyField('accounts.UserAccount', through='ShiftRegistration', related_name='shifts')
    # to set only if created from template. But really useful? Maybe just more complexity
    # origin_event = models.ForeignKey("RecurringEvent", null=True, verbose_name=_(u''), help_text=_(u''))
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=20000, blank=True)
    slot_amount = models.IntegerField(verbose_name=_(u'number of needed volunteers'))
    start_time = models.DateTimeField(verbose_name=_('starting time'), db_index=True)
    end_time = models.DateTimeField(verbose_name=_('ending time'), db_index=True)
    created_at = models.DateTimeField(verbose_name=_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name=_('updated at'), auto_now=True)
    published_at = models.DateTimeField(verbose_name=_('published at'), null=True)
    cancelled_at = models.DateTimeField(verbose_name=_('cancelled at'), null=True)
    # shift_slug = models.CharField(max_length=255)

    shifts = NeedManager()
    open_shifts = OpenShiftManager()

    # @property
    # def slugify(self):
    #     return '{}-{}:{}'.format(self.start_time.isoformat(), self.start_time, self.end_time.hours, self.end_time.minutes)

    def save(self, *args, **kwargs):
        # self.shift_slug = self.slugify
        self.save(*args, **kwargs)
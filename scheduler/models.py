# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
import locale
import datetime


class Need(models.Model):
    """
    This is the primary instance to create shifts
    """
    class Meta:
        verbose_name = _("shift")
        verbose_name_plural = _("shifts")
    topic = models.ForeignKey("Topics", verbose_name=_("helptype"), help_text=_("helptype_text"))
    location = models.ForeignKey('Location', verbose_name=_("location"))
    time_period_from = models.ForeignKey("TimePeriods", related_name="time_from", verbose_name=_("time from"))
    time_period_to = models.ForeignKey("TimePeriods", related_name="time_to")

    # Currently required. If you want to allow not setting this, make sure to update
    # associated logic where slots is used.
    slots = models.IntegerField(verbose_name=_("number of needed volunteers"))

    def get_volunteer_total(self):
        return self.registrationprofile_set.all().count()
    get_volunteer_total.short_description = _("assigned volunteers")

    def get_volunteers(self):
        return self.registrationprofile_set.all()
    get_volunteers.short_description = _("volunteers")

    # Two properties to make accessing the timestamps slightly saner.
    # TODO: Just remove the ForeignKey relationship and replace with datetime fields, and give
    #       it the fields the names of the properties. But don't mess up the necessary
    #       data migration. ;)
    @property
    def start(self):
        return self.time_period_from.date_time

    @property
    def end(self):
        return self.time_period_to.date_time

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
        latest_start_time = self.start + grace
        earliest_end_time = self.end - grace
        if earliest_end_time <= latest_start_time:
            # Event is shorter than 2 * grace time, can't have overlaps.
            return []

        return [
            need for need in needs
            if (need.start < latest_start_time < need.end) or
               (latest_start_time < need.start < earliest_end_time)
        ]

    def __unicode__(self):
        return self.topic.title + " " + self.location.name


class Topics(models.Model):
    class Meta:
        verbose_name = _("helptype")
        verbose_name_plural = _("helptypes")

    title = models.CharField(max_length=255)
    description = models.TextField(max_length=20000, blank=True)

    def __unicode__(self):
        return self.title

    def get_current_needs_py_topic(self):
        return self.need_set.all()


class TimePeriods(models.Model):
    class Meta:
        verbose_name = _("timeperiod")
        verbose_name_plural = _("timeperiods")

    date_time = models.DateTimeField()

    def __unicode__(self):
        return str(self.date_time)


class Location(models.Model):

    name = models.CharField(max_length=255, blank=True)
    street = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=255, blank=True)
    postal_code = models.CharField(max_length=5, blank=True)
    latitude = models.CharField(max_length=30, blank=True)
    longitude = models.CharField(max_length=30, blank=True)
    additional_info = models.TextField(max_length=300000, blank=True)

    class Meta:
        verbose_name = _("location")
        verbose_name_plural = _("locations")
        permissions = (
            ("can_view", "User can view location"),
        )

    def __unicode__(self):
        return self.name

    def get_dates_of_needs(self):
        needs_dates = []
        for i in self.need_set.all().filter(time_period_to__date_time__gt=datetime.datetime.now())\
                .order_by('time_period_to__date_time'):
            date_name = i.time_period_from.date_time.strftime("%A, %d.%m.%Y")
            locale.setlocale(locale.LC_ALL, 'de_DE.UTF-8')
            if date_name not in needs_dates:
                needs_dates.append(i.time_period_from.date_time.strftime("%A, %d.%m.%Y"))
        return needs_dates

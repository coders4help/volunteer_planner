# -*- coding: utf-8 -*-
from django.db import models
import locale
from django.contrib.auth.models import User
from django.template.defaultfilters import date as _date
import datetime

from registration.models import RegistrationProfile


class Need(models.Model):
    """
    This is the primary instance to create shifts
    """
    class Meta:
        verbose_name = "Schicht"
        verbose_name_plural = "Schichten"
    topic = models.ForeignKey("Topics", verbose_name="Hilfetyp", help_text=u"Jeder Hilfetyp hat so viele Planelemente "
                                                                           u"wie es Arbeitsschichten geben soll. Dies ist "
                                                                           u"EINE Arbeitsschicht für einen bestimmten Tag")
    location = models.ForeignKey('Location', verbose_name="Ort")
    time_period_from = models.ForeignKey("TimePeriods", related_name="time_from", verbose_name="Anfangszeit")
    time_period_to = models.ForeignKey("TimePeriods", related_name="time_to")
    slots = models.IntegerField(blank=True, verbose_name="Anz. benoetigter Freiwillige")
    achivated = models.BooleanField(default=False)

    def get_volunteer_total(self):
        return self.registrationprofile_set.all().count()
    get_volunteer_total.short_description = "Reg. Freiwillige"

    def get_volunteers(self):
        return self.registrationprofile_set.all()
    get_volunteers.short_description = "Freiwillige"

    def __unicode__(self):
        return self.topic.title + " " + self.location.name


class scheduledRegPro(models.Model):
    """
    This is the connection between a user and the shift to which he/she has signed up
    """
    registration_profile = models.ForeignKey(RegistrationProfile, on_delete=models.CASCADE)
    need = models.ForeignKey(Need, on_delete=models.CASCADE)
    did_show_up = models.BooleanField(default=False)


class Topics(models.Model):
    class Meta:
        verbose_name = "Hilfebereich"
        verbose_name_plural = "Hilfebereiche"

    title = models.CharField(max_length=255)
    description = models.TextField(max_length=20000, blank=True)

    def __unicode__(self):
        return self.title

    def get_current_needs_py_topic(self):
        return self.need_set.all()


class TimePeriods(models.Model):
    class Meta:
        verbose_name = "Zeitspanne"
        verbose_name_plural = "Zeitspannen"

    date_time = models.DateTimeField()

    def __unicode__(self):
        return str(self.date_time)


class Location(models.Model):

    class Meta:
        verbose_name = "Ort"
        verbose_name_plural = "Orte"
        permissions = (
            ("can_view", "User can view location"),
            ("can_checkin", "Can checkin volunteers"),
        )

    name = models.CharField(max_length=255, blank=True)
    street = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=255, blank=True)
    postal_code = models.CharField(max_length=5, blank=True)
    longitude = models.CharField(max_length=30, blank=True)
    altitude = models.CharField(max_length=30, blank=True)
    additional_info = models.TextField(max_length=300000, blank=True)

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

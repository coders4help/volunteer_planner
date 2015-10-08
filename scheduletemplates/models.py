# coding: utf-8
from datetime import timedelta

from django.db import models
from django.utils.translation import ugettext_lazy as _


class ScheduleTemplate(models.Model):
    name = models.CharField(max_length=256, verbose_name=_('name'))


class ShiftTemplate(models.Model):
    schedule = models.ForeignKey('scheduletemplates.ScheduleTemplate',
                                 verbose_name=_('schedule'),
                                 )

    facility = models.ForeignKey('organizations.Facility',
                                 verbose_name=_(u'facility'),
                                 related_name='shift_templates')

    task = models.ForeignKey('organizations.Task',
                             verbose_name=_(u'task'),
                             related_name='+')

    workplace = models.ForeignKey('organizations.Workplace',
                                  verbose_name=_(u'workplace'),
                                  related_name='+',
                                  null=True,
                                  blank=True)

    starting_time = models.TimeField(verbose_name=_('starting time'),
                                     db_index=True)

    ending_time = models.TimeField(verbose_name=_('ending time'),
                                   db_index=True)

    days = models.PositiveIntegerField(verbose_name=_(u'days'),
                                       default=0)

    slots = models.IntegerField(verbose_name=_(u'number of needed volunteers'))

    @property
    def duration(self):
        return (timedelta(days=self.days) + timedelta(
            hours=self.ending_time.hour,
            minutes=self.ending_time.minute)) - timedelta(
            hours=self.starting_time.hour, minutes=self.starting_time.minute)

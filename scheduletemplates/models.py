# coding: utf-8
from datetime import timedelta, datetime, time

from django.db import models
from django.templatetags.l10n import localize
from django.utils.translation import gettext_lazy as _

from . import managers


class ScheduleTemplate(models.Model):
    name = models.CharField(max_length=256, verbose_name=_('name'))

    facility = models.ForeignKey('organizations.Facility',
                                 models.CASCADE,
                                 verbose_name=_(u'facility'),
                                 related_name='schedule_templates')

    class Meta:
        ordering = ('facility',)
        verbose_name_plural = _('schedule templates')
        verbose_name = _('schedule template')

    def __unicode__(self):
        return u'{}'.format(self.name)

    def __str__(self):
        return self.__unicode__()


class ShiftTemplate(models.Model):
    schedule_template = models.ForeignKey('scheduletemplates.ScheduleTemplate',
                                          models.CASCADE,
                                          verbose_name=_('schedule template'),
                                          related_name='shift_templates'
                                          )

    slots = models.IntegerField(verbose_name=_(u'number of needed volunteers'))

    task = models.ForeignKey('organizations.Task',
                             models.CASCADE,
                             verbose_name=_(u'task'), )

    workplace = models.ForeignKey('organizations.Workplace',
                                  models.CASCADE,
                                  verbose_name=_(u'workplace'),
                                  null=True,
                                  blank=True)

    starting_time = models.TimeField(verbose_name=_('starting time'),
                                     db_index=True)

    ending_time = models.TimeField(verbose_name=_('ending time'),
                                   db_index=True)

    days = models.PositiveIntegerField(verbose_name=_(u'days'),
                                       default=0)

    members_only = models.BooleanField(default=False,
                                       verbose_name=_(u'members only'),
                                       help_text=_(
                                           u'allow only members to help'))

    objects = managers.ShiftTemplateManager()

    class Meta:
        ordering = ('schedule_template',)
        verbose_name_plural = _('shift templates')
        verbose_name = _('shift template')

    @property
    def duration(self):
        today = datetime.today()
        days = timedelta(days=self.days)
        start = datetime.combine(today, self.starting_time)
        end = datetime.combine(today + days, self.ending_time)
        duration = end - start
        return duration

    @property
    def localized_display_ending_time(self):
        days = self.days if self.ending_time > time.min else 0
        days_fmt = _(u'after {number_of_days} days'.format(number_of_days=days))
        days_str = days_fmt.format(
            number_of_days=days) if days else u''
        return u'{time} {days}'.format(time=localize(self.ending_time),
                                       days=days_str).strip()

    @property
    def summary(self):
        return u'{}: {} x {}{} from {} to {}'.format(self.schedule_template,
                                                     self.slots,
                                                     self.task.name,
                                                     self.workplace and u'/{}'.format(
                                                         self.workplace.name) or u'',
                                                     self.starting_time,
                                                     self.localized_display_ending_time)

    def __unicode__(self):

        if self.workplace:
            return _(u"{task_name} - {workplace_name}").format(
                task_name=self.task.name,
                workplace_name=self.workplace.name)
        else:
            return _(u"{task_name}").format(task_name=self.task.name)

    def __str__(self):
        return self.__unicode__()

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.days == 0 and self.starting_time >= self.ending_time:
            self.days = 1
        super(ShiftTemplate, self).save(force_insert=force_insert,
                                        force_update=force_update,
                                        using=using,
                                        update_fields=update_fields)

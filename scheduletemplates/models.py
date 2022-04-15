from datetime import datetime, time, timedelta

from django.core.validators import MinValueValidator
from django.db import models
from django.templatetags.l10n import localize
from django.utils import timezone
from django.utils.timezone import get_current_timezone, make_aware
from django.utils.translation import gettext_lazy as _, ngettext_lazy

from . import managers


class ScheduleTemplate(models.Model):
    name = models.CharField(max_length=256, verbose_name=_("name"))

    facility = models.ForeignKey(
        "organizations.Facility",
        models.CASCADE,
        verbose_name=_("facility"),
        related_name="schedule_templates",
    )

    class Meta:
        ordering = ("facility",)
        verbose_name_plural = _("schedule templates")
        verbose_name = _("schedule template")

    def __unicode__(self):
        return "{}".format(self.name)

    def __str__(self):
        return self.__unicode__()


class ShiftTemplate(models.Model):
    schedule_template = models.ForeignKey(
        "scheduletemplates.ScheduleTemplate",
        models.CASCADE,
        verbose_name=_("schedule template"),
        related_name="shift_templates",
    )

    slots = models.PositiveIntegerField(
        verbose_name=_("slots"),
        help_text=_("number of needed volunteers"),
        validators=[
            MinValueValidator(1),
        ],
    )

    task = models.ForeignKey(
        "organizations.Task",
        models.CASCADE,
        verbose_name=_("task"),
    )

    workplace = models.ForeignKey(
        "organizations.Workplace",
        models.CASCADE,
        verbose_name=_("workplace"),
        null=True,
        blank=True,
    )

    starting_time = models.TimeField(verbose_name=_("starting time"), db_index=True)
    ending_time = models.TimeField(verbose_name=_("ending time"), db_index=True)

    days = models.PositiveIntegerField(verbose_name=_("days"), default=0)

    members_only = models.BooleanField(
        default=False,
        verbose_name=_("members only"),
        help_text=_("allow only members to help"),
    )

    objects = managers.ShiftTemplateManager()

    class Meta:
        ordering = ("schedule_template",)
        verbose_name_plural = _("shift templates")
        verbose_name = _("shift template")

    @property
    def duration(self):
        today = timezone.now().date()
        start = datetime.combine(today, self.starting_time)
        end = datetime.combine(today + timedelta(days=self.days), self.ending_time)
        duration = end - start
        return duration

    @property
    def localized_display_ending_time(self):
        days = self.days if self.ending_time > time.min else 0
        days_fmt = ngettext_lazy("the next day", "after {number_of_days} days", days)
        days_str = days_fmt.format(number_of_days=days) if days else ""
        return "{time} {days}".format(
            time=localize(
                make_aware(self.ending_time, timezone=get_current_timezone())
            ),
            days=days_str,
        ).strip()

    @property
    def summary(self):
        return "{}: {} x {}{} from {} to {}".format(
            self.schedule_template,
            self.slots,
            self.task.name,
            self.workplace and "/{}".format(self.workplace.name) or "",
            make_aware(self.starting_time, timezone=get_current_timezone()),
            self.localized_display_ending_time,
        )

    def __unicode__(self):
        if self.workplace:
            return f"{self.task.name} - {self.workplace.name}"
        else:
            return f"{self.task.name}"

    def __str__(self):
        return self.__unicode__()

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        if self.days == 0 and self.starting_time >= self.ending_time:
            self.days = 1
        super(ShiftTemplate, self).save(
            force_insert=force_insert,
            force_update=force_update,
            using=using,
            update_fields=update_fields,
        )

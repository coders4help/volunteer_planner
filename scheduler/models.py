# coding: utf-8
import logging
from datetime import time

from django.core.validators import MinValueValidator
from django.db import models
from django.urls import reverse
from django.utils.formats import localize
from django.utils.timezone import get_current_timezone, localtime
from django.utils.translation import gettext_lazy as _, ngettext_lazy

from . import managers

logger = logging.getLogger(__name__)


class Shift(models.Model):
    """A Shift is a time period for the work on a task at a workplace of a
        certain facility (see organizations). Users register themselves for
        shifts, but there can be more than one slot for a shift, ie. there
        can be more than one user for a shift.

    fields:
        slots - depending on how many volunteers are needed to fulfill the
            task
        task - foreign key to organizations-Task
        workplace - foreign key to organizations-Workplace
        facility - foreign key to organizations-Facility
        starting_time
        ending_time
        helpers - many2many to accounts-UserAccount, realized through
            ShiftHelper
        members_only - if only members are allowed to help

    The manager is extended via managers.ShiftManager.
    A second manager open_shifts is set to managers.OpenShiftManager.

    Defines three properties:
        days
        duration
        localized_display_ending_time

    """

    # PositiveIntegerField instead of custom validation
    slots = models.PositiveIntegerField(
        verbose_name=_("slots"),
        help_text=_("number of needed volunteers"),
        validators=[
            MinValueValidator(1),
        ],
    )

    task = models.ForeignKey(
        "organizations.Task", models.PROTECT, verbose_name=_("task")
    )
    workplace = models.ForeignKey(
        "organizations.Workplace",
        models.PROTECT,
        verbose_name=_("workplace"),
        null=True,
        blank=True,
    )

    facility = models.ForeignKey(
        "organizations.Facility", models.PROTECT, verbose_name=_("facility")
    )

    starting_time = models.DateTimeField(verbose_name=_("starting time"), db_index=True)
    ending_time = models.DateTimeField(verbose_name=_("ending time"), db_index=True)

    helpers = models.ManyToManyField(
        "accounts.UserAccount", through="ShiftHelper", related_name="shifts"
    )

    members_only = models.BooleanField(
        default=False,
        verbose_name=_("members only"),
        help_text=_("allow only members to help"),
    )

    objects = managers.ShiftManager()
    open_shifts = managers.OpenShiftManager()

    class Meta:
        verbose_name = _("shift")
        verbose_name_plural = _("shifts")
        ordering = ["starting_time", "ending_time"]

    @property
    def days(self):
        return (self.ending_time.date() - self.starting_time.date()).days

    @property
    def duration(self):
        return self.ending_time - self.starting_time

    @property
    def localized_display_ending_time(self):
        days = self.days if self.ending_time.time() > time.min else 0
        days_fmt = ngettext_lazy("the next day", "after {number_of_days} days", days)
        days_str = days_fmt.format(number_of_days=days) if days else ""
        return "{time} {days}".format(
            time=localize(localtime(self.ending_time, get_current_timezone()).time()),
            days=days_str,
        ).strip()

    def __unicode__(self):
        return "{title} - {facility} ({start} - {end})".format(
            title=self.task.name,
            facility=self.facility.name,
            start=localize(localtime(self.starting_time, get_current_timezone())),
            end=localize(localtime(self.ending_time, get_current_timezone())),
        )

    def __str__(self):
        return self.__unicode__()

    def get_absolute_url(self):
        local_starting_time = localtime(self.starting_time, get_current_timezone())
        return reverse(
            "shift_details",
            kwargs=dict(
                facility_slug=self.facility.slug,
                year=local_starting_time.year,
                month=local_starting_time.month,
                day=local_starting_time.day,
                shift_id=self.id,
            ),
        )


class ShiftHelper(models.Model):
    """A user registered for a shift. There is a many2many relationship
        between shift and user. ShiftHelper is the data structure realizing
        this relationship.

    fields:
    user_account - foreign key to accounts.UserAccount
    shift - foreign key to Shift
    joined_shift_at - datetime with auto_now_add set True, ie. a timestamp
        for when the user registered for the shift

    Manager is set to managers.ShiftHelperManager.
    """

    user_account = models.ForeignKey(
        "accounts.UserAccount", models.CASCADE, related_name="shift_helpers"
    )
    shift = models.ForeignKey(
        "scheduler.Shift", models.CASCADE, related_name="shift_helpers"
    )
    joined_shift_at = models.DateTimeField(auto_now_add=True)

    objects = managers.ShiftHelperManager()

    class Meta:
        verbose_name = _("shift helper")
        verbose_name_plural = _("shift helpers")
        unique_together = ("user_account", "shift")

    def __unicode__(self):
        return "{} on {}".format(self.user_account.user.username, self.shift.task)

    def __str__(self):
        return self.__unicode__()


class ShiftMessageToHelpers(models.Model):
    """
    The ShiftMessageToHelpers represents a message to be sent to the helpers
    signed up for a certain shift. A use case would be to tell all helpers to
    come 1 hour later.

    The actual email will be sent via a post_save signal.
    """

    class Meta:
        verbose_name = ngettext_lazy("shift notification", "shift notifications", 1)
        verbose_name_plural = ngettext_lazy(
            "shift notification", "shift notifications", 2
        )

    message = models.TextField(verbose_name=_("Message"))
    sender = models.ForeignKey(
        "accounts.UserAccount",
        null=True,
        on_delete=models.SET_NULL,
        related_name="msg_sender",
        verbose_name=_("sender"),
    )
    send_date = models.DateTimeField(auto_now_add=True, verbose_name=_("send date"))
    shift = models.ForeignKey(
        "Shift", on_delete=models.CASCADE, verbose_name=_("Shift")
    )
    recipients = models.ManyToManyField(
        "accounts.UserAccount", verbose_name=_("recipients")
    )

    def __str__(self):
        return "{} on {}".format(self.sender.user.email, self.shift.task)

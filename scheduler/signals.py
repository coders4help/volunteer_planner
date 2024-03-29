from common import brace_format_logging

from django.conf import settings
from django.core.mail import EmailMessage
from django.db.models.signals import pre_delete, pre_save, post_save
from django.dispatch import receiver
from django.template.defaultfilters import time as date_filter
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.timezone import timedelta
from django.utils.translation import gettext_lazy as _

from scheduler.models import Shift, ShiftMessageToHelpers

logger = brace_format_logging.getLogger(__name__)


@receiver(pre_delete, sender=Shift)
def send_email_notifications(sender, instance, **kwargs):
    """
    HACK ALERT

    This needed to be done quickly. Please use a proper email template,
    add some error handling, some sane max recipient handling, tests, etc.

    Also: No try/except

    sender : request.user  # WTF? Is that a wish? A question? A prayer? :/
    """
    try:
        shift = instance
        if shift.ending_time >= timezone.now():
            subject = "Schicht am {} wurde abgesagt".format(
                shift.starting_time.strftime("%d.%m.%y")
            )

            message = render_to_string(
                "shift_cancellation_notification.html", {"shift": shift}
            )

            from_email = settings.DEFAULT_FROM_EMAIL
            # TODO: identify current manager or give facility an e-mail address
            reply_to = ["kontakt@volunteer-planner.org"]
            addresses = shift.helpers.values_list("user__email", flat=True)

            if addresses:
                mail = EmailMessage(
                    subject=subject,
                    body=message,
                    to=["kontakt@volunteer-planner.org"],
                    from_email=from_email,
                    bcc=addresses,
                    reply_to=reply_to,
                )
                mail.send()
    except Exception:
        logger.exception(
            "Error sending notification email (Shift: {shift})",
            shift=instance,
        )


def times_changed(shift, old_shift, grace=None):
    grace = grace if grace is not None else timedelta(minutes=5)
    starting_time = min(shift.starting_time, shift.ending_time)
    ending_time = max(shift.starting_time, shift.ending_time)

    old_starting_time = min(old_shift.starting_time, old_shift.ending_time)
    old_ending_time = max(old_shift.starting_time, old_shift.ending_time)

    starting_diff = max(old_starting_time, starting_time) - min(
        old_starting_time, starting_time
    )
    ending_diff = max(old_ending_time, ending_time) - min(old_ending_time, ending_time)

    return ending_diff > grace or starting_diff > grace


@receiver(pre_save, sender=Shift)
def notify_users_shift_change(sender, instance, **kwargs):
    shift = instance
    if shift.pk:
        old_shift = Shift.objects.get(pk=shift.pk)

        if old_shift.starting_time >= timezone.now() and times_changed(
            shift, old_shift
        ):
            subject = "Schicht wurde verändert: {task} am {date}".format(
                task=old_shift.task.name, date=date_filter(old_shift.starting_time)
            )

            message = render_to_string(
                "shift_modification_notification.html",
                {
                    "old": old_shift,
                    "shift": shift,
                },
            )

            from_email = settings.DEFAULT_FROM_EMAIL

            addresses = shift.helpers.values_list("user__email", flat=True)
            if addresses:
                mail = EmailMessage(
                    subject=subject,
                    body=message,
                    to=["kontakt@volunteer-planner.org"],
                    from_email=from_email,
                    bcc=addresses,
                )
                logger.info(
                    "Shift {} at {} changed: ({}-{} -> {}->{}). Sending email "
                    "notification to {} affected user(s).",
                    shift.task.name,
                    shift.facility.name,
                    old_shift.starting_time,
                    old_shift.ending_time,
                    shift.starting_time,
                    shift.ending_time,
                    len(addresses),
                )
                mail.send()


@receiver(post_save, sender=ShiftMessageToHelpers)
def send_shift_message_to_helpers(sender, instance, created, **kwargs):
    if not created:
        for recipient in instance.recipients.all():
            if instance.sender.user.email:
                try:
                    message = render_to_string(
                        "emails/shift_message_to_helpers.txt",
                        {
                            "message": instance.message,
                            "recipient": recipient,
                            "shift": instance.shift,
                            "sender_email": instance.sender.user.email,
                        },
                    ).strip()
                    subject = _(
                        "Volunteer-Planner: A Message from shift "
                        "manager of {shift_title}"
                    ).format(shift_title=instance.shift.task.name)
                    if message:
                        mail = EmailMessage(
                            subject=subject,
                            body=message,
                            to=[recipient.user.email],
                            from_email="noreply@volunteer-planner.org",
                            reply_to=(instance.sender.user.email,),
                            headers={"Reply-to": instance.sender.user.email},
                        )
                        mail.send()
                except Exception:
                    logger.exception(
                        "send_shift_message_to_helpers: message not successful",
                    )

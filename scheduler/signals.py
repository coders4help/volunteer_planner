# coding=utf-8
import logging
from django.utils.timezone import timedelta

from django.conf import settings
from django.core.mail import EmailMessage
from django.db.models.signals import pre_delete, pre_save
from django.dispatch import receiver
from django.template.defaultfilters import time as date_filter
from django.template.loader import render_to_string
from django.utils import timezone

from scheduler.models import Shift

logger = logging.getLogger(__name__)


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
            subject = u'Schicht am {} wurde abgesagt'.format(
                shift.starting_time.strftime('%d.%m.%y'))

            message = render_to_string('shift_cancellation_notification.html',
                                       dict(shift=shift))

            from_email = settings.DEFAULT_FROM_EMAIL
            # TODO Find a way to identify current manager or give facility an e-mail address
            reply_to = ['kontakt@volunteer-planner.org']
            addresses = shift.helpers.values_list('user__email', flat=True)

            if addresses:
                mail = EmailMessage(subject=subject, body=message,
                                    to=['kontakt@volunteer-planner.org'],
                                    from_email=from_email,
                                    bcc=addresses,
                                    reply_to=reply_to)
                mail.send()
    except Exception as e:
        logger.exception("Error sending notification email (Shift: %s)" % instance)
        pass


def times_changed(shift, old_shift, grace=timedelta(minutes=5)):
    starting_time = min(shift.starting_time, shift.ending_time)
    ending_time = max(shift.starting_time, shift.ending_time)

    old_starting_time = min(old_shift.starting_time, old_shift.ending_time)
    old_ending_time = max(old_shift.starting_time, old_shift.ending_time)

    starting_diff = max(old_starting_time, starting_time) - min(
        old_starting_time, starting_time)
    ending_diff = max(old_ending_time, ending_time) - min(
        old_ending_time, ending_time)

    return ending_diff > grace or starting_diff > grace


@receiver(pre_save, sender=Shift)
def notify_users_shift_change(sender, instance, **kwargs):
    shift = instance
    if shift.pk:
        old_shift = Shift.objects.get(pk=shift.pk)

        if old_shift.starting_time >= timezone.now() and times_changed(shift,
                                                                       old_shift):
            subject = u'Schicht wurde verändert: {task} am {date}'.format(
                task=old_shift.task.name,
                date=date_filter(old_shift.starting_time))

            message = render_to_string('shift_modification_notification.html',
                                       dict(old=old_shift, shift=shift))

            from_email = settings.DEFAULT_FROM_EMAIL

            addresses = shift.helpers.values_list('user__email', flat=True)
            if addresses:
                mail = EmailMessage(subject=subject,
                                    body=message,
                                    to=['kontakt@volunteer-planner.org'],
                                    from_email=from_email,
                                    bcc=addresses)
                logger.info(
                    u'Shift %s at %s changed: (%s-%s -> %s->%s). Sending email notification to %d affected user(s).',
                    shift.task.name, shift.facility.name,
                    old_shift.starting_time, old_shift.ending_time,
                    shift.starting_time, shift.ending_time,
                    len(addresses))
                mail.send()

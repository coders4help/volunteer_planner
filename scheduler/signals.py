# coding=utf-8
import logging
from datetime import datetime

from django.template.defaultfilters import time as date_filter
from django.core.mail import EmailMessage
from django.db.models.signals import pre_delete, pre_save
from django.dispatch import receiver
from django.template.loader import render_to_string

from scheduler.models import Shift

logger = logging.getLogger(__name__)
grace = 5 * 60  # 5 minutes in seconds


@receiver(pre_delete, sender=Shift)
def send_email_notifications(sender, instance, **kwargs):
    """
    HACK ALERT

    This needed to be done quickly. Please use a proper email template,
    add some error handling, some sane max recipient handling, tests, etc.
    """
    shift = instance
    if shift.ending_time >= datetime.now():
        subject = u'Schicht am {} wurde abgesagt'.format(
            shift.starting_time.strftime('%d.%m.%y'))

        message = render_to_string('shift_cancellation_notification.html',
                                   dict(shift=shift))

        from_email = "Volunteer-Planner.org <noreply@volunteer-planner.org>"

        addresses = shift.helpers.values_list('user__email', flat=True)

        if addresses:
            mail = EmailMessage(subject=subject, body=message,
                                to=['support@volunteer-planner.org'],
                                from_email=from_email,
                                bcc=addresses)
            mail.send()


@receiver(pre_save, sender=Shift)
def notify_users_shift_change(sender, instance, **kwargs):
    shift = instance

    if shift.pk:
        old_shift = Shift.objects.get(pk=shift.pk)

        # Test whether this is modification or creation, to avoid DoesNotExist exception
        if old_shift.ending_time >= datetime.now():

            subject = u'Schicht wurde verändert: {task} am {date}'.format(
                task=old_shift.task.name,
                date=date_filter(old_shift.starting_time))

            message = render_to_string('shift_modification_notification.html',
                                       dict(old=old_shift, shift=shift))

            from_email = "Volunteer-Planner.org <noreply@volunteer-planner.org>"

            addresses = shift.helpers.values_list('user__email', flat=True)
            if addresses:
                mail = EmailMessage(subject=subject,
                                    body=message,
                                    to=['support@volunteer-planner.org'],
                                    from_email=from_email,
                                    bcc=addresses)
                logger.info(
                    u'Shift %s at %s changed: (%s-%s -> %s->%s). Sending email notification to %d affected user(s).',
                    shift.task.name, shift.facility.name,
                    old_shift.starting_time, old_shift.ending_time,
                    shift.starting_time, shift.ending_time,
                    len(addresses))
                mail.send()

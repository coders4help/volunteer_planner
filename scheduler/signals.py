# coding=utf-8
from django.core.mail import EmailMessage
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.template.loader import render_to_string

from scheduler.models import Need


@receiver(pre_delete, sender=Need)
def send_email_notifications(sender, instance, **kwargs):
    """
    HACK ALERT

    This needed to be done quickly. Please use a proper email template,
    add some error handling, some sane max recipient handling, tests, etc.
    """
    shift = instance
    subject = u'Schicht am {} wurde abgesagt'.format()

    message = render_to_string('shift_cancellation_notification.html', dict(shift=shift))

    from_email = "Volunteer-Planner.org <noreply@volunteer-planner.org>"

    addresses = shift.registrationprofile_set.values_list('user__email',
                                                          flat=True)

    mail = EmailMessage(subject=subject, body=message,
                        to=['support@volunteer-planner.org'],
                        from_email=from_email,
                        bcc=addresses)
    mail.send()
